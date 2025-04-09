const express = require('express');
const app = express();
const PORT = 5000;

// 設定 GET 路由，當訪問根路徑 (/) 時返回訊息
app.get('/', (req, res) => {
    res.send('代購網站後端啟動成功');
});

// 啟動伺服器，監聽指定的端口
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
