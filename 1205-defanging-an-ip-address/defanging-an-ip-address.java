class Solution {
    public String defangIPaddr(String address) {
        StringBuilder ans = new StringBuilder();
        for (int i = 0; i < address.length(); i++) {
            char ch = address.charAt(i);

            if (ch == '.') {
                ans.append("[.]");
            } else {
                ans.append(ch);
            }
        }
        return ans.toString();
    }
}