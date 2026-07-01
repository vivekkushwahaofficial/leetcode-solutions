class Solution {
    public double findMaxAverage(int[] nums, int k) {
        int low = 0;
        int high = k - 1;
        double sum = 0;
        for (int i = 0; i < k; i++) {
            sum = sum + nums[i];
        }
        double res = sum;
        while (high < nums.length - 1) {
            sum = sum - nums[low] + nums[high + 1];

            res = Math.max(res, sum);
            low++;
            high++;
        }
        double avg = res / k;

        return avg;
    }
}