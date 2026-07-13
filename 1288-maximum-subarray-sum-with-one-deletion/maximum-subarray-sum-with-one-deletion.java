class Solution {
    public int maximumSum(int[] arr) {

        int nodelete = arr[0];
        int onedelete = Integer.MIN_VALUE;
        int res = arr[0];

        for (int i = 1; i < arr.length; i++) {

            int prevnodelete = nodelete;
            int prevonedelete = onedelete;

            // Maximum sum without deletion
            nodelete = Math.max(prevnodelete + arr[i], arr[i]);

            int v2;

            // First time deleting current element
            if (prevonedelete == Integer.MIN_VALUE) {
                v2 = prevnodelete;
            } else {
                // Already deleted one element earlier
                v2 = prevonedelete + arr[i];
            }

            // Either delete current element or extend deleted subarray
            onedelete = Math.max(prevnodelete, v2);

            res = Math.max(res, Math.max(nodelete, onedelete));
        }

        return res;
    }
}