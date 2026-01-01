#include <bits/stdc++.h>
using namespace std;

// 极快验证：利用构造特性，无需检查所有区间
bool is_valid(const vector<int>& p, const vector<int>& ones, int k, int n, const string& s) {
    for (int pos : ones) {
        int val = p[pos];
        int min_l = max(0, pos - k + 1);
        int max_l = min(pos, n - k);
        
        if (min_l > max_l) continue; // 没有包含该位置的长度为k的区间
        
        // 只需检查区间内是否有'0'位置（这些位置的值更大）
        bool has_larger = false;
        
        // 检查左侧是否有'0'
        if (pos > 0) {
            int left_end = max(min_l, pos - 1);
            for (int i = pos - 1; i >= left_end; --i) {
                if (s[i] == '0') { // '0'位置的值一定大于'1'位置
                    has_larger = true;
                    break;
                }
            }
        }
        
        // 左侧没有则检查右侧
        if (!has_larger && pos < n - 1) {
            int right_start = min(max_l, pos + 1);
            for (int i = pos + 1; i <= right_start + k - 1; ++i) {
                if (i >= n) break;
                if (s[i] == '0') { // '0'位置的值一定大于'1'位置
                    has_larger = true;
                    break;
                }
            }
        }
        
        if (!has_larger) return false;
    }
    return true;
}

void solve() {
    int n, k;
    string s;
    cin >> n >> k >> s;

    vector<int> ones;
    for (int i = 0; i < n; ++i) {
        if (s[i] == '1') {
            ones.push_back(i);
        }
    }

    // 情况1：k=1时，'1'位置必然是长度1区间的最大值
    if (k == 1) {
        if (ones.empty()) {
            cout << "YES\n";
            for (int i = 1; i <= n; ++i) cout << i << " ";
        } else {
            cout << "NO\n";
        }
        cout << "\n";
        return;
    }

    // 情况2：k > n时，不存在长度为k的区间
    if (k > n) {
        cout << "YES\n";
        for (int i = 1; i <= n; ++i) cout << i << " ";
        cout << "\n";
        return;
    }

    // 快速可行性检查：每个'1'的区间内必须有'0'
    bool possible = true;
    for (int pos : ones) {
        int min_l = max(0, pos - k + 1);
        int max_l = min(pos, n - k);
        if (min_l > max_l) continue;
        
        bool has_zero = false;
        // 检查区间内是否有至少一个'0'
        int start = min_l;
        int end = max_l + k - 1;
        // 优化：只检查'1'位置周围的关键区域
        int check_start = max(start, pos - 1);
        int check_end = min(end, pos + 1);
        
        if (check_start <= check_end) {
            for (int i = check_start; i <= check_end; ++i) {
                if (s[i] == '0') {
                    has_zero = true;
                    break;
                }
            }
        }
        
        if (!has_zero) {
            possible = false;
            break;
        }
    }

    if (!possible) {
        cout << "NO\n";
        return;
    }

    // 构造排列：'1'用较小值，'0'用较大值（利用这一特性加速验证）
    vector<int> p(n);
    int small = 1, large = n;

    // 先填充'1'的位置
    for (int i = 0; i < n; ++i) {
        if (s[i] == '1') {
            p[i] = small++;
        }
    }

    // 再填充'0'的位置（从右向左）
    for (int i = n-1; i >= 0; --i) {
        if (s[i] == '0') {
            p[i] = large--;
        }
    }

    // 验证（利用构造特性，验证速度极快）
    if (is_valid(p, ones, k, n, s)) {
        cout << "YES\n";
        for (int num : p) {
            cout << num << " ";
        }
        cout << "\n";
    } else {
        // 尝试从左向右填充'0'
        large = n;
        for (int i = 0; i < n; ++i) {
            if (s[i] == '0') {
                p[i] = large--;
            }
        }
        
        if (is_valid(p, ones, k, n, s)) {
            cout << "YES\n";
            for (int num : p) {
                cout << num << " ";
            }
            cout << "\n";
        } else {
            cout << "NO\n";
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        solve();
    }

    return 0;
}
    