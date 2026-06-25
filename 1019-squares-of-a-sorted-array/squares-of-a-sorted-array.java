class Solution {
    public int[] sortedSquares(int[] nums) {
        int arr[] = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            arr[i] = nums[i] * nums[i];
        }
        // Arrays.sort(arr);
        int start = 0;
        int end = arr.length - 1;
        while (start < end) {
            for (int i = 0; i < end; i++) {
                if (arr[i] > arr[i + 1]) {
                    int temp = arr[i];
                    arr[i] = arr[i + 1];
                    arr[i + 1] = temp;
                } else {
                    continue;
                }
            }
            end --;
        }
        return arr;
    }
}