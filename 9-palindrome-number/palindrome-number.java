class Solution {
    public boolean isPalindrome(int x) {
        int originalNum = x;
        int revNum = 0;
        if(x < 0){
            return false;
        }
        while (x > 0) {
            int rem = x % 10;
            x = x / 10;
            revNum = revNum * 10 + rem;
        }
        if (revNum != originalNum) {
            return false;
        }
        return true;
    }
}