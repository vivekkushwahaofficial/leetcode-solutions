class Solution {
    public int mySqrt(int x) {
        if (x == 0) {
            return 0;
        }
        int low = 1;
        int high = x;
        int mid = 0;
        int answer = 0;

        while (low <= high) {
            mid = low + (high - low) / 2;
            long square = (long)mid * mid;
            if (square == x) {
                return mid;
            } else if (square < x) {
                answer = mid;
                low = mid + 1;

            } else {
                high = mid - 1;
            }
        }
        return answer;
    }
}