class Solution {
    public int[] sortedSquares(int[] nums) {
        // int arr[] = new int[nums.length];
        // for (int i = 0; i < nums.length; i++) {
        //     arr[i] = nums[i] * nums[i];
        // }
        // Arrays.sort(arr);
        // return arr;
        int start = 0;
        int end = nums.length - 1;
        int[] arr = new int[nums.length];
        int idx = nums.length - 1;
        while (start <= end) {
            int leftSquare = nums[start] * nums[start];
            int rightSquare = nums[end] * nums[end];

            if (leftSquare > rightSquare) {
                arr[idx] = leftSquare;
                start++;
            } else {
                arr[idx] = rightSquare;
                end--;
            }
            idx--;
        }

        return arr;
    }
}