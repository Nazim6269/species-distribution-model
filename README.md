## Results

- 839 oriole records after thinning, 1,218 background points
  (other birds, same 5 km thinning)
- Mean climate of oriole and background nearly identical
- Random split AUC 0.315 (invalid: identical climate values appear in
  both training and test with opposite labels). Shuffled-label control: 0.499
- Spatial block CV AUC: 0.525 (folds 0.507 to 0.539)
- Conclusion: six WorldClim variables do not distinguish oriole
  records from the background in Bangladesh
