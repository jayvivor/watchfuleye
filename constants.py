# Player naming
with open("playernames.txt","r+") as player_names:
    gender_neutral_names = [name[:-1] for name in player_names.readlines()]

self_snitch_constant = 70

# Utils
stat_max = 100

# Insight
insight_half_life = .5
insight_trust_threshold = .5
insight_trust_scale = 20

# Reads
read_fuzz = 5
read_fuzz_scale = .1
sus_scale = .2

# Relationships
first_impression_cap = 20
bond_build_fuzz = 10  # How wildly different bonds will improve/worsen over time.

# General
default_cast_size = 16

# Timestamps
hours_per_day = 10