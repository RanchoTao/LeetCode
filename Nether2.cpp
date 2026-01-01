#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int query(int x, vector<int> S) {
    cout << "? " << x << " " << S.size();
    for (int node : S) {
        cout << " " << node;
    }
    cout << endl;
    cout.flush();
    int res;
    cin >> res;
    return res;
}

void solve() {
    int n;
    cin >> n;

    vector<int> fullSet;
    for (int i = 1; i <= n; i++) {
        fullSet.push_back(i);
    }

    vector<int> dp(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        dp[i] = query(i, fullSet);
    }

    vector<vector<int>> groups(n + 1);
    int max_dp = 0;
    for (int i = 1; i <= n; i++) {
        if (dp[i] > max_dp) {
            max_dp = dp[i];
        }
        groups[dp[i]].push_back(i);
    }

    vector<int> path;
    if (!groups[max_dp].empty()) {
        sort(groups[max_dp].begin(), groups[max_dp].end());
        path.push_back(groups[max_dp][0]);
    } else {
        return;
    }

    for (int d = max_dp - 1; d >= 1; d--) {
        if (groups[d].empty()) {
            break;
        }
        sort(groups[d].begin(), groups[d].end());
        int u = path.back();
        int next_node = -1;
        for (int v : groups[d]) {
            vector<int> S = {u, v};
            int res = query(u, S);
            if (res == 2) {
                next_node = v;
                break;
            }
        }
        if (next_node == -1) {
            next_node = groups[d][0];
        }
        path.push_back(next_node);
    }

    cout << "! " << path.size();
    for (int node : path) {
        cout << " " << node;
    }
    cout << endl;
    cout.flush();
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}