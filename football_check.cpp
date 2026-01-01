#include <iostream>
#include <algorithm>
using namespace std;

// 检查一个半场的进球序列是否合法（没有连续3次同一队进球）
// 更可靠的方法：判断是否任何一队的进球数都不超过另一队的2倍+2
bool check_half(int goals_r, int goals_k) {
    // 基本条件：两队进球总数为0一定合法
    if (goals_r == 0 && goals_k == 0) return true;
    
    // 关键判断：任何一队的进球数不能比另一队多太多
    // 如果一队进球数 > 另一队进球数×2 + 2，则必然出现连续3次进球
    if (goals_r > 2 * goals_k + 2) return false;
    if (goals_k > 2 * goals_r + 2) return false;
    
    return true;
}

int main() {
    int t;
    cin >> t;
    
    while (t--) {
        int a, b, c, d;
        cin >> a >> b >> c >> d;
        
        // 基本条件检查：上半场进球不能超过全场
        if (a > c || b > d) {
            cout << "no" << endl;
            continue;
        }
        
        // 计算上下半场的进球数
        int r1 = a, k1 = b;          // 上半场
        int r2 = c - a, k2 = d - b;  // 下半场
        
        // 检查上下半场是否都合法
        bool valid_first = check_half(r1, k1);
        bool valid_second = check_half(r2, k2);
        
        if (valid_first && valid_second) {
            cout << "yes" << endl;
        } else {
            cout << "no" << endl;
        }
    }
    
    return 0;
}
    