#include <algorithm>
#include <cstring> // 用于 memset

using namespace std;

const int N = 256; // 扩展为256以覆盖所有ASCII字符

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        if (s.empty()) return 0;
        
        bool exist[N];
        memset(exist, false, sizeof(exist)); // 初始化数组
        
        int res = 0;
        int i = 0, j = 0;
        
        for (; j < s.size(); j++) {
            char ch = s[j];
            // 如果当前字符已存在，移动左指针直到移除重复字符
            while (exist[ch]) {
                exist[s[i]] = false;
                i++;
            }
            
            exist[ch] = true;
            res = max(res, j - i + 1);
        }
        
        return res;
    }
};