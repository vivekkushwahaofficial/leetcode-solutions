class Solution {
    public int maxSubarraySumCircular(int[] nums) {
        int bestEnding1 = nums[0];
        int bestEnding2 = nums[0];
        int total = nums[0];
        int sum1 = nums[0];
        int sum2 = nums[0];
        int sum3 = nums[0];

        for(int i = 1; i < nums.length; i++){
            int v1 = bestEnding1 + nums[i];
            int v2 = nums[i];
            bestEnding1 = Math.max(v1, v2);
            sum1 = Math.max(bestEnding1, sum1);
        }
        for(int i = 1; i < nums.length; i++){
            int v1 = bestEnding2 + nums[i];
            int v2 = nums[i];
            bestEnding2 = Math.min(v1, v2);
            sum2 = Math.min(bestEnding2, sum2);
        }
        for(int i = 1; i < nums.length; i++){
            total = total + nums[i];
        }
        sum3 = total - sum2;
        if(total == sum2){
            return sum1;
        }
        return Math.max(sum1, sum3);
    }
}