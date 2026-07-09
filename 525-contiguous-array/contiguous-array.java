class Solution {
    public int findMaxLength(int[] nums) {
        int sum = 0;
        int maxLength = 0;
        int currLength = 0;

        HashMap<Integer, Integer> map = new HashMap<>();
        map.put(0, -1);

        for (int i = 0; i < nums.length; i++) {
            if (nums[i] == 0) {
                sum += -1;
            } else {
                sum++;
            }

            if (map.containsKey(sum)) {
                currLength = i - map.get(sum);
            } else {
                map.put(sum, i);
            }

            maxLength = Math.max(maxLength, currLength);
        }
        return maxLength;
    }
}