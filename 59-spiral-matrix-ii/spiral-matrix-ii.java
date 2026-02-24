class Solution {
    public int[][] generateMatrix(int n) {
        int[][] arr = new int[n][n];
        int count = 1;
        int minRow = 0;
        int maxRow = n-1;
        int minCol = 0;
        int maxCol = n-1;
        while(count <= n*n){
            for(int a=minCol; a<=maxCol; a++){
                arr[minRow][a] = count;
                count++;
            }
            for(int b=minRow+1; b<=maxRow; b++){
                arr[b][maxCol] = count;
                count++;
            }
            for(int a=maxCol-1; a>=minCol; a--){
                arr[maxRow][a] = count;
                count++;
            }
               for(int b=maxRow-1; b>=minRow+1; b--){
                arr[b][minCol] = count;
                count++;
            }

            minCol++;
            maxCol--;
            minRow++;
            maxRow--;
            
        }
        return arr;
    }
}