class Solution {
    public int findDuplicate(int[] nums) {
        // int ans = 0;
        // for (int i = 0; i < nums.length; i++) {
        //     int ele = nums[i];
        //     ele = Math.abs(ele);

        //     if (nums[ele] > 0) {
        //         nums[ele] = -nums[ele];
        //     } else {
        //         ans = ele;
        //         break;
        //     }
        // }
        // for (int i = 0; i < nums.length; i++) {
        //     nums[i] = Math.abs(nums[i]);
        // }
        // return ans;

        // HashSet<Integer> seen = new HashSet<>();
        // for (int i = 0; i < nums.length; i++) {
        //     if (seen.contains(nums[i])) {
        //         return nums[i];
        //     }
        //     seen.add(nums[i]);
        // }
        // return -1;

        int slow = nums[0];
        int fast = nums[0];

        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        slow = nums[0];

        while(slow != fast){
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
}