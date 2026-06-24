class Solution {
    public int dominantIndex(int[] nums) {
        int largest = nums[0];
        int idx = 0;
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > largest) {
                largest = nums[i];
                idx = i;
            }
        }
        for (int j = 0; j < nums.length; j++) {
            if (j == idx) {
                continue;
            }
            if (largest < 2 * nums[j]) {
                return -1;
            }
        }
        return idx;
    }
}