import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extract_stellar_ai_save_model_evidence import (  # noqa: E402
    build_snapshot,
    render_csv,
    render_json,
)


META = '''
version="Pegasus v4.4.4"
version_control_revision=28
name="Synthetic Evidence Save"
date="2250.01.01"
'''

GAMESTATE = '''
version="Pegasus v4.4.4"
date="2250.01.01"
decoy={
  country={
    999={
      type=default
      military_power=999999
    }
  }
  fleet_template={
    999={ fleet_size=999 }
  }
}
country=
{
  1={
    name={ key="Synthetic AI" type=planet }
    type=default
    last_date_was_human="0.01.01"
    personality="honorbound_warriors"
    military_power=1096.45
    fleet_size=130
    economy_power=1200
    tech_power=800
    used_naval_capacity=80
    navy_coverage=0.5
    num_sapient_pops=1234
    ethos={
      ethic="ethic_fanatic_militarist"
      ethic="ethic_authoritarian"
    }
    government={
      type="gov_military_dictatorship"
      authority="auth_dictatorial"
      origin="origin_default"
      civics={
        "civic_distinguished_admiralty"
        "civic_nationalistic_zeal"
      }
    }
    budget={
      current_month={
        balance={
          country_base={ alloys=5 }
          planet_metallurgists={ alloys=12.5 }
          ships={ alloys=-5 }
        }
      }
    }
    modules={
      standard_economy_module={
        resources={ alloys=250 }
      }
    }
    controlled_colonies={ 7 8 }
    fleets_manager={
      owned_fleets={
        { fleet=10 }
        { fleet=11 }
        { fleet=12 ownership_status=lost_control }
      }
    }
    fleet_template_manager={ fleet_template={ 20 } }
  }
  2={
    name={ key="Prior Human" }
    type=default
    last_date_was_human="2200.01.01"
    military_power=0
    fleet_size=0
    economy_power=1
    tech_power=1
    used_naval_capacity=0
    navy_coverage=0
    num_sapient_pops=1
    budget={ current_month={ balance={ country_base={ alloys=1 } } } }
    modules={ standard_economy_module={ resources={ alloys=5 } } }
    controlled_colonies={ 9 }
    fleets_manager={ owned_fleets={ } }
    fleet_template_manager={ fleet_template={ } }
  }
  3={
    name={ key="Fallen Decoy" }
    type=fallen_empire
    military_power=750000
    fleet_size=2500
  }
}
construction=
{
  queue_mgr={
    queues={
      30={
        items={ 100 101 }
        owner=1
        simultaneous=3
        type=ships
      }
      31={
        owner=1
        simultaneous=1
        type=starbase
      }
    }
  }
}
ships={ }
fleet=
{
  10={
    ships={ 1 2 3 }
    ship_class=shipclass_military
    military_power=1096.45
  }
  11={
    ships={ 4 }
    ship_class=shipclass_starbase
    military_power=500
  }
  12={
    ships={ 5 6 7 8 }
    ship_class=shipclass_military
    military_power=9999
  }
}
fleet_template=
{
  20={
    fleet=10
    fleet_template_design={
      {
        ship_design_implementation={ design=1 upgrade=4294967295 growth_stage=0 }
        count=5
      }
    }
    all_queued={ }
    fleet_size=50
  }
}
'''


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class StellarAiSaveModelEvidenceTests(unittest.TestCase):
    def make_save(self, root: Path) -> Path:
        save_path = root / "synthetic.sav"
        with zipfile.ZipFile(save_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("meta", META)
            archive.writestr("gamestate", GAMESTATE)
        return save_path

    def test_nested_type_traps_are_ignored_and_only_top_level_default_countries_are_emitted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            snapshot = build_snapshot(self.make_save(Path(temp_dir)))

        self.assertEqual(snapshot["summary"]["normal_default_empire_count"], 2)
        self.assertEqual([row["country_id"] for row in snapshot["empires"]], ["1", "2"])
        self.assertEqual(snapshot["empires"][0]["country_type"], "default")
        self.assertNotIn("999", [row["country_id"] for row in snapshot["empires"]])

    def test_military_power_is_never_taken_from_fleet_size(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            snapshot = build_snapshot(self.make_save(Path(temp_dir)))

        empire = snapshot["empires"][0]
        self.assertEqual(empire["military_power"], 1096.45)
        self.assertEqual(empire["fleet_size_not_power"], 130.0)
        self.assertEqual(snapshot["parser"]["military_power_source"], "country.military_power")

    def test_economy_fleet_template_and_shipyard_evidence_are_extracted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            snapshot = build_snapshot(self.make_save(Path(temp_dir)))

        empire = snapshot["empires"][0]
        self.assertEqual(empire["alloy_stockpile"], 250.0)
        self.assertEqual(empire["alloy_net_income"], 12.5)
        self.assertEqual(empire["systems"], 1)
        self.assertEqual(empire["colonies"], 2)
        self.assertEqual(empire["military_ship_count"], 3)
        self.assertEqual(empire["mobile_military_fleet_count"], 1)
        self.assertEqual(empire["fleet_template_target_ship_count"], 5)
        self.assertEqual(empire["fleet_template_current_ship_count"], 3)
        self.assertEqual(empire["fleet_template_reinforcement_demand_ship_count"], 2)
        self.assertEqual(empire["shipyard_parallel_capacity"], 3)
        self.assertEqual(empire["ship_construction_items_queued"], 2)
        self.assertEqual(empire["shipyard_active_slots"], 2)
        self.assertEqual(empire["shipyard_active_utilization"], 0.66667)
        self.assertEqual(empire["naval_capacity_estimate_from_coverage"], 160.0)

    def test_human_history_is_proven_but_no_human_history_remains_an_ai_candidate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            snapshot = build_snapshot(self.make_save(Path(temp_dir)))

        ai_candidate, prior_human = snapshot["empires"]
        self.assertEqual(
            ai_candidate["control_classification"],
            "ai_candidate_no_human_history_recorded",
        )
        self.assertEqual(
            ai_candidate["control_classification_certainty"],
            "current_controller_uncertain",
        )
        self.assertEqual(prior_human["control_classification"], "player_or_previously_human")
        self.assertEqual(prior_human["control_classification_certainty"], "proven_human_history")

    def test_extraction_is_read_only_and_serialization_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            save_path = self.make_save(Path(temp_dir))
            before = file_sha256(save_path)
            first = build_snapshot(save_path)
            second = build_snapshot(save_path)
            after = file_sha256(save_path)

        self.assertEqual(before, after)
        self.assertEqual(render_json(first), render_json(second))
        self.assertEqual(render_csv(first), render_csv(second))
        self.assertEqual(json.loads(render_json(first))["input"]["sha256"], before.upper())


if __name__ == "__main__":
    unittest.main()
