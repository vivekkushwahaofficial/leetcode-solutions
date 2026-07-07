class Solution {
    public boolean containsDuplicate(int[] nums) {
        Arrays.sort(nums);
        for (int index = 0; index < nums.length - 1; index++) {
            if (nums[index] == nums[index + 1]) {
                return true;
            }
        }
        return false;
    }
}