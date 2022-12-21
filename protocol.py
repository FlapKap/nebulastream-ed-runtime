import minipb

# schema
# should correspond to
# message output_entry_schema {
#   int key = 1;
#   bytes value = 2;
# }
# message output_entry {
#   repeated output_entry_schema = 1;
# }

output_entry_schema = (("key", "z"), ("value", "a"),)
output_schema = (("values", "+[", output_entry_schema, "]"),)

calculator_schema = (("instructions", "+z"))

filter_schema = (("predicate", calculator_schema))
map_schema = (("function", calculator_schema))


