class Solution {
    public int[] twoSum(int[] nums, int target) {
        for(int i = 0; i < nums.length; i++){
            for(int j = i + 1; j < nums.length; j++){
                if(nums[i] + nums[j] == target){
                    return new int[]{i, j};
                }
            }
        }

        // HashMap<Integer, Integer> map = new HashMap<>();
        // for (int i = 0; i < nums.length; i++) {
        //     int result = target - nums[i];
        //     if (map.containsKey(result)) {
        //         return new int[] { map.get(result), i };
        //     }
        //     map.put(nums[i], i);
        // }
        return new int[]{ -1, -1 };
    }
}