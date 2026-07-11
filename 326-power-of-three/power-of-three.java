class Solution {

    public boolean isPowerOfThree(int n) {

        // Base case: 1 is 3^0
        if (n == 1) {
            return true;
        }

        // If n is less than 1 or not divisible by 3,
        // it cannot be a power of 3.
        if (n <= 0 || n % 3 != 0) {
            return false;
        }

        // Recursive call with a smaller problem
        return isPowerOfThree(n / 3);
    }
}