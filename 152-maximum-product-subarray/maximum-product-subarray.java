class Solution {
    public int maxProduct(int[] nums) {
        int largestProduct = nums[0];
        int leastProduct = nums[0];
        int ans = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int v1 = nums[i];
            int v2 = largestProduct * nums[i];
            int v3 = leastProduct * nums[i];

            largestProduct = Math.max(v1, Math.max(v2, v3));
            leastProduct = Math.min(v1, Math.min(v2, v3));

            ans = Math.max(ans, Math.max(largestProduct, leastProduct));
        }
        return ans;
    }
}