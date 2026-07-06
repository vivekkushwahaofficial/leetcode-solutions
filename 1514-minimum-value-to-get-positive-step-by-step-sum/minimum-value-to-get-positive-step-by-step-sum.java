class Solution {
    public int minStartValue(int[] nums) {
        int sum = 0;
        int minSum = 0;

        // for (int i = 0; i <= nums.length - 1; i++) {
        //     sum += nums[i];
        //     minSum = Math.min(minSum, sum);
        // }
        for (int num : nums) {
            sum += num;
            minSum = Math.min(minSum, sum);
        }
        return 1 - minSum;
    }
}