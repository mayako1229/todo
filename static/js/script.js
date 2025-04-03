
// ドラッグ＆ドロップで順番を変更
new Sortable(document.getElementById('sortable'), {
    onEnd: function (evt) {
        let order = [];
        document.querySelectorAll('#sortable tr').forEach((row, index) => {
            order.push({ id: row.getAttribute('data-id'), position: index + 1 });
        });
        updateOrder(order);
    }
});

// 順番を更新する関数
function updateOrder(order) {
    fetch('/update_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order: order })
    });
}

// 完了したタスクを削除
document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function () {
        let taskId = this.getAttribute('data-id');
        fetch('/delete_task/' + taskId, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => location.reload());
    });
});

// ゴミ箱ボタンで完了したタスクを削除
document.getElementById('clear-completed-btn').addEventListener('click', function () {
    fetch('/delete_completed_tasks', { method: 'DELETE' })
        .then(response => response.json())
        .then(data => location.reload());
});
// タスク完了処理
document.querySelectorAll('.complete-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', async function () {
        let taskId = this.getAttribute('data-id');
        let completed = this.checked;

        try {
            let response = await fetch('/complete_task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ task_id: taskId, completed: completed })
            });

            if (!response.ok) {
                throw new Error('サーバーエラーが発生しました');
            }

            let data = await response.json();
            console.log('完了処理成功:', data);

            // 成功したらページをリロード
            location.reload();
        } catch (error) {
            console.error('エラー:', error);
        }
    });
});
