let gameState = null;
let selectedPiece = null;
let validMoves = [];
let attackTargets = [];
let currentTurn = 'chaos';
let currentPlayerName = 'Хаос';
let selectedWeaponType = 'melee';
let selectedWeaponIndex = 0;

async function init() {
    await loadGameState();
    await loadCurrentTurn();
    renderBoard();
    updateTurnIndicator();
}

async function loadGameState() {
    const response = await fetch('/api/game/state');
    gameState = await response.json();
}

async function loadCurrentTurn() {
    const response = await fetch('/api/game/turn');
    const data = await response.json();
    currentTurn = data.current_turn;
    currentPlayerName = data.current_player;
}

function updateTurnIndicator() {
    const turnText = document.getElementById('turn-text');

    if (currentTurn === 'chaos') {
        turnText.textContent = `🟣 Ход: ${currentPlayerName}`;
        turnText.className = '';
    } else {
        turnText.textContent = `🔵 Ход: ${currentPlayerName}`;
        turnText.className = 'space-marines';
    }
}

async function switchTurn() {
    if (selectedPiece) {
        if (!confirm('⚠️ Передать ход?')) {
            return;
        }
    }

    const response = await fetch('/api/game/switch-turn', { method: 'POST' });
    const result = await response.json();

    if (response.ok) {
        addToBattleLog({ type: 'turn', message: `➡️ ${result.message}` });
        await init();
        deselectPiece();
        checkGameEnd();
    } else {
        alert('❌ Ошибка: ' + result.detail);
    }
}

function renderBoard() {
    const board = document.getElementById('game-board');
    board.innerHTML = '';

    const pieceMap = {};
    gameState.pieces.forEach(piece => {
        // Сохраняем информацию о базе для каждой модели
        pieceMap[`${piece.row},${piece.col}`] = piece;
    });

    for (let row = 0; row < gameState.rows; row++) {
        for (let col = 0; col < gameState.cols; col++) {
            const cell = document.createElement('div');
            cell.className = 'cell';

            const piece = pieceMap[`${row},${col}`];

            if (selectedPiece && selectedPiece.row === row && selectedPiece.col === col) {
                cell.classList.add('selected');
            }

            if (validMoves.some(m => m.row === row && m.col === col)) {
                cell.classList.add('valid-move');
            }

            if (attackTargets.some(t => t.row === row && t.col === col)) {
                cell.classList.add('attack-target');
            }

            // Подсветка клеток, занимаемых базами моделей
            gameState.pieces.forEach(p => {
                const halfBase = (p.base_size - 1) / 2;
                const minRow = Math.floor(p.row - halfBase);
                const maxRow = Math.ceil(p.row + halfBase + p.base_size - 1 - 2 * halfBase - 0.001);
                const minCol = Math.floor(p.col - halfBase);
                const maxCol = Math.ceil(p.col + halfBase + p.base_size - 1 - 2 * halfBase - 0.001);
                
                if (row >= minRow && row < maxRow && col >= minCol && col < maxCol) {
                    if (p.base_size >= 3) {
                        cell.classList.add('occupied-large');
                    } else if (p.base_size === 2) {
                        cell.classList.add('occupied-medium');
                    }
                }
            });

            if (piece) {
                const pieceEl = document.createElement('div');
                // Добавляем класс размера базы к иконке
                const baseSizeClass = piece.base_size >= 3 ? 'piece-large' : 
                                     piece.base_size === 2 ? 'piece-medium' : 'piece-small';
                pieceEl.className = `piece ${piece.faction} ${baseSizeClass}`;
                pieceEl.textContent = piece.symbol;

                if (piece.W_max > 0) {
                    const healthBar = document.createElement('div');
                    healthBar.className = 'health-bar';
                    const healthFill = document.createElement('div');
                    healthFill.className = 'health-fill';
                    healthFill.style.width = `${(piece.W / piece.W_max) * 100}%`;
                    healthBar.appendChild(healthFill);
                    cell.appendChild(healthBar);
                }

                cell.appendChild(pieceEl);
            }

            cell.onclick = () => onCellClick(row, col, piece);
            board.appendChild(cell);
        }
    }
}

async function onCellClick(row, col, piece) {
    if (!selectedPiece) {
        if (piece && piece.faction === currentTurn) {
            await selectPiece(piece);
        } else if (piece) {
            showPieceInfo(piece);
        }
        return;
    }

    if (piece) {
        const isTarget = attackTargets.some(t => t.row === row && t.col === col);
        if (isTarget && piece.faction !== currentTurn) {
            await attackPiece(selectedPiece.id, piece.id);
            return;
        }

        if (piece.faction === currentTurn) {
            await selectPiece(piece);
            return;
        }

        showPieceInfo(piece);
        return;
    }

    const isValidMove = validMoves.some(m => m.row === row && m.col === col);
    if (isValidMove) {
        await movePiece(selectedPiece.id, row, col);
        return;
    }

    deselectPiece();
}

// ✅ ИСПРАВЛЕНО: Выбор оружия перед атакой
async function selectPiece(piece) {
    selectedPiece = piece;
    selectedWeaponType = 'melee';
    selectedWeaponIndex = 0;

    await loadAttacksForCurrentWeapon();
    renderBoard();
    showPieceInfo(piece);
}

async function loadAttacksForCurrentWeapon() {
    if (!selectedPiece) return;
    
    const [movesRes, targetsRes] = await Promise.all([
        fetch(`/api/game/piece/${selectedPiece.id}/moves`),
        fetch(`/api/game/piece/${selectedPiece.id}/targets?weapon_type=${selectedWeaponType}&weapon_index=${selectedWeaponIndex}`)
    ]);

    const movesData = await movesRes.json();
    const targetsData = await targetsRes.json();

    validMoves = movesData.moves || [];
    attackTargets = targetsData.targets || [];
}

async function movePiece(pieceId, newRow, newCol) {
    const response = await fetch('/api/game/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ piece_id: pieceId, new_row: newRow, new_col: newCol })
    });

    if (response.ok) {
        addToBattleLog({ type: 'move', message: `🚶 ${selectedPiece.name} → (${newRow}, ${newCol})` });
        await init();
        deselectPiece();
    } else {
        const error = await response.json();
        alert('❌ Ошибка: ' + error.detail);
    }
}

async function attackPiece(attackerId, defenderId) {
    const defender = gameState.pieces.find(p => p.id === defenderId);

    // ✅ Показываем какое оружие используется
    const weapon = selectedWeaponType === 'range'
        ? selectedPiece.RangeWeapon[selectedWeaponIndex]
        : selectedPiece.MeleeWeapon[selectedWeaponIndex];

    if (!confirm(`⚔️ Атаковать ${defender.name} оружием "${weapon.name}"?\nДальность: ${weapon.R || 1}"`)) {
        return;
    }

    const response = await fetch('/api/game/attack', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            attacker_id: attackerId,
            defender_id: defenderId,
            weapon_type: selectedWeaponType,
            weapon_index: selectedWeaponIndex
        })
    });

    const result = await response.json();

    if (response.ok) {
        const log = result.attack_log || {};
        const logMessage = result.killed
            ? `💀 ${selectedPiece.name} (${log.weapon_name}) уничтожил ${defender.name}!`
            : `⚔️ ${selectedPiece.name} (${log.weapon_name}): ${log.hits} попаданий, ${log.wounds} ранений, ${log.total_damage} урона`;

        addToBattleLog({ type: 'attack', message: logMessage });
        await init();
        deselectPiece();
        checkGameEnd();
    } else {
        alert('❌ Ошибка: ' + result.detail);
    }
}

// ✅ ИСПРАВЛЕНО: Выбор оружия из досье
function selectWeapon(weaponType, weaponIndex) {
    selectedWeaponType = weaponType;
    selectedWeaponIndex = weaponIndex;
    loadAttacksForCurrentWeapon();
    renderBoard();
    showPieceInfo(selectedPiece);
}

function showPieceInfo(piece) {
    const isMyPiece = piece.faction === currentTurn;
    const factionName = piece.faction === 'chaos' ? '🟣 Хаос' : '🔵 Космодесант';
    const factionClass = piece.faction === 'chaos' ? '' : 'space-marines';

    let weaponsHtml = '';

    // Дальний бой
    if (piece.RangeWeapon && piece.RangeWeapon.length > 0) {
        weaponsHtml += '<div class="wh40k-section"><div class="wh40k-section-title">🎯 Дальний Бой</div>';
        piece.RangeWeapon.forEach((w, idx) => {
            const isSelected = selectedWeaponType === 'range' && selectedWeaponIndex === idx && isMyPiece;
            weaponsHtml += `
                <div class="wh40k-weapon ${isSelected ? 'selected-weapon' : ''}" ${isMyPiece ? `onclick="selectWeapon('range', ${idx})"` : ''} style="${isMyPiece ? 'cursor: pointer;' : ''}">
                    <div class="wh40k-weapon-name">${w.name} ${isSelected ? '✅' : ''}</div>
                    <div class="wh40k-weapon-stats">
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">R</span><span class="wh40k-weapon-stat-value">${w.R}"</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">A</span><span class="wh40k-weapon-stat-value">${w.AN}</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">BS</span><span class="wh40k-weapon-stat-value">${w.BS}+</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">S</span><span class="wh40k-weapon-stat-value">${w.S}</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">AP</span><span class="wh40k-weapon-stat-value">${w.AP}</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">D</span><span class="wh40k-weapon-stat-value">${w.D}</span></div>
                    </div>
                    ${w.keywords && w.keywords.length > 0 ? `
                        <div class="wh40k-keywords">
                            ${w.keywords.map(k => `<span class="wh40k-keyword">${k}</span>`).join('')}
                        </div>
                    ` : ''}
                </div>
            `;
        });
        weaponsHtml += '</div>';
    }

    // Ближний бой
    if (piece.MeleeWeapon && piece.MeleeWeapon.length > 0) {
        weaponsHtml += '<div class="wh40k-section"><div class="wh40k-section-title">⚔️ Ближний Бой</div>';
        piece.MeleeWeapon.forEach((w, idx) => {
            const isSelected = selectedWeaponType === 'melee' && selectedWeaponIndex === idx && isMyPiece;
            weaponsHtml += `
                <div class="wh40k-weapon ${isSelected ? 'selected-weapon' : ''}" ${isMyPiece ? `onclick="selectWeapon('melee', ${idx})"` : ''} style="${isMyPiece ? 'cursor: pointer;' : ''}">
                    <div class="wh40k-weapon-name">${w.name} ${isSelected ? '✅' : ''}</div>
                    <div class="wh40k-weapon-stats">
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">A</span><span class="wh40k-weapon-stat-value">${w.AN}</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">WS</span><span class="wh40k-weapon-stat-value">${w.WS}+</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">S</span><span class="wh40k-weapon-stat-value">${w.S}</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">AP</span><span class="wh40k-weapon-stat-value">${w.AP}</span></div>
                        <div class="wh40k-weapon-stat"><span class="wh40k-weapon-stat-label">D</span><span class="wh40k-weapon-stat-value">${w.D}</span></div>
                    </div>
                    ${w.keywords && w.keywords.length > 0 ? `
                        <div class="wh40k-keywords">
                            ${w.keywords.map(k => `<span class="wh40k-keyword">${k}</span>`).join('')}
                        </div>
                    ` : ''}
                </div>
            `;
        });
        weaponsHtml += '</div>';
    }

    const infoHtml = `
        <div class="wh40k-character-name">${piece.name}</div>
        <div class="wh40k-faction ${factionClass}">${factionName}</div>

        <div class="wh40k-stats-grid">
            <div class="wh40k-stat"><span class="wh40k-stat-label">M</span><span class="wh40k-stat-value">${piece.M}</span></div>
            <div class="wh40k-stat"><span class="wh40k-stat-label">T</span><span class="wh40k-stat-value">${piece.T}</span></div>
            <div class="wh40k-stat"><span class="wh40k-stat-label">SV</span><span class="wh40k-stat-value">${piece.SV}+</span></div>
            <div class="wh40k-stat"><span class="wh40k-stat-label">ISV</span><span class="wh40k-stat-value">${piece.ISV || '-'}</span></div>
            <div class="wh40k-stat"><span class="wh40k-stat-label">W</span><span class="wh40k-stat-value">${piece.W}</span></div>
            <div class="wh40k-stat"><span class="wh40k-stat-label">LD</span><span class="wh40k-stat-value">${piece.LD}</span></div>
            <div class="wh40k-stat"><span class="wh40k-stat-label">OC</span><span class="wh40k-stat-value">${piece.OC}</span></div>
            <div class="wh40k-stat"><span class="wh40k-stat-label">Тип</span><span class="wh40k-stat-value">${piece.type}</span></div>
        </div>

        <div class="wh40k-wounds-bar">
            <div class="bar-container">
                <div class="bar-fill" style="width: ${(piece.W / piece.W_max) * 100}%"></div>
            </div>
            <div class="wh40k-wounds-text">${piece.W} / ${piece.W_max} Ран</div>
        </div>

        ${weaponsHtml}

        ${piece.keywords && piece.keywords.length > 0 ? `
            <div class="wh40k-section">
                <div class="wh40k-section-title">🏷️ Ключевые Слова</div>
                <div class="wh40k-keywords">
                    ${piece.keywords.map(k => `<span class="wh40k-keyword">${k}</span>`).join('')}
                </div>
            </div>
        ` : ''}

        <div class="action-buttons">
            ${isMyPiece ? `
                ${attackTargets.length > 0 ? '<button class="btn-action attack" onclick="alert(\'Кликните на красную ячейку для атаки выбранным оружием\')">⚔️ Атаковать</button>' : ''}
                ${validMoves.length > 0 ? '<button class="btn-action move" onclick="alert(\'Кликните на зелёную ячейку для перемещения\')">🚶 Движение (M=' + piece.M + ')</button>' : ''}
                <button class="btn-action" onclick="switchTurn()">➡️ Передать ход</button>
            ` : ''}
            <button class="btn-action" onclick="deselectPiece()">✖️ Закрыть</button>
        </div>
    `;

    document.getElementById('piece-info').innerHTML = infoHtml;
}

function deselectPiece() {
    selectedPiece = null;
    validMoves = [];
    attackTargets = [];
    renderBoard();
    document.getElementById('piece-info').innerHTML = '<p class="hint">Кликните на персонажа для просмотра</p>';
}

function addToBattleLog(entry) {
    const logContent = document.getElementById('log-content');
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${entry.type}`;
    logEntry.textContent = entry.message;
    logContent.insertBefore(logEntry, logContent.firstChild);

    while (logContent.children.length > 30) {
        logContent.removeChild(logContent.lastChild);
    }
}

function checkGameEnd() {
    const chaosPieces = gameState.pieces.filter(p => p.faction === 'chaos');
    const smPieces = gameState.pieces.filter(p => p.faction === 'space_marines');

    if (chaosPieces.length === 0) {
        alert('🏆 Space Marines победили! За Империум!');
        addToBattleLog({ type: 'info', message: '🏆 SPACE MARINES ПОБЕДИЛИ!' });
    } else if (smPieces.length === 0) {
        alert('🏆 Хаос победил! Слава Темным Богам!');
        addToBattleLog({ type: 'info', message: '🏆 ХАОС ПОБЕДИЛ!' });
    }
}

async function resetGame() {
    if (confirm('🔄 Начать новую битву?')) {
        await fetch('/api/game/reset', { method: 'POST' });
        addToBattleLog({ type: 'info', message: '🔄 Новая битва началась' });
        await init();
        deselectPiece();
    }
}

window.onload = init;