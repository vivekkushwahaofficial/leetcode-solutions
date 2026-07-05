class Solution {
    public int mySqrt(int x) {

        // Handle the special case
        if (x == 0) {
            return 0;
        }

        int low = 1;
        int high = x;
        int answer = 0;

        while (low <= high) {

            // Find the middle element
            int mid = low + (high - low) / 2;

            // Use long to avoid integer overflow
            long square = (long) mid * mid;

            if (square == x) {
                return mid; // Perfect square found
            } 
            else if (square < x) {
                answer = mid;      // Store possible answer
                low = mid + 1;     // Search on the right
            } 
            else {
                high = mid - 1;    // Search on the left
            }
        }

        // Return the floor value of the square root
        return answer;
    }
}