/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
#include <bits/c++.h>
using namespace std;
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        queue<TreeNode *> levelQueue;
        vector<vector<int>> ans;
        vector<int> currLevel;
        if(root == NULL){
            return ans;
        }
        int level = 0;
        levelQueue.push(root);
        levelQueue.push(NULL);
        TreeNode *curr;
        while(!levelQueue.empty()){
            curr = levelQueue.front();
            levelQueue.pop();
            if(curr == NULL){
                level++;
                ans.push_back(currLevel);
                currLevel.clear();
                if(!levelQueue.empty()){
                    levelQueue.push(NULL);
                }
            }
            else{
                currLevel.push_back(curr->val);
                if(curr->left){
                    levelQueue.push(curr->left);
                }
                if(curr->right){
                    levelQueue.push(curr->right);
                }
            }
        }
        // cout << level << endl;
        return ans;
    }
};