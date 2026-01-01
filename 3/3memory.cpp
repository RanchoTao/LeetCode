class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        vector<int> an(128,0);
        int ma=0,l=0;
        for(int i=0;i<s.size();i++)
        {
            l=max(l,an[s[i]]);
            an[s[i]]=i+1;
            ma=max(ma,i-l+1);
        }
        return ma;
    }
};