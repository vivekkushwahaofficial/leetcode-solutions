class Solution {
    public String interpret(String command) {
        StringBuilder ans = new StringBuilder();
        for (int i = 0; i < command.length(); i++) {
            char ch = command.charAt(i);

            if (ch == 'G') {
                ans.append("G");
            } else if (ch == '(' && command.charAt(i + 1) == ')') {
                ans.append("o");
                i++;
            } else {
                ans.append("al");
                i += 3;
            }
        }
        return ans.toString();
    }
}