class Solution {
    public String removeDuplicates(String s) {
        Stack<Character> st = new Stack<>();
        StringBuilder res = new StringBuilder();

        for (int i = 0; i < s.length(); i++) {
            if (st.empty()) {
                st.push(s.charAt(i));
            } else if (st.peek() == s.charAt(i)) {
                st.pop();
            } else {
                st.push(s.charAt(i));
            }
        }

        while (!st.empty()) {
            res.append(st.pop());
        }

return res.reverse().toString();    }
}