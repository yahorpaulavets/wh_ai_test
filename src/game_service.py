import random
from typing import Optional, List

from src.models import GamePiece, PieceType, PieceFaction, RangeWeapon, MeleeWeapon


class GameService:
    def __init__(self):
        self.state_rows = 44
        self.state_cols = 60
        self.pieces: List[GamePiece] = []
        self.current_turn = PieceFaction.CHAOS
        self._initialize_pieces()

    def _initialize_pieces(self):
        """Создать персонажей в стиле Warhammer 40K"""
        self.pieces = [
            # 🟣 Игрок 1 - Chaos Daemons
            GamePiece(
                id="chaos_prince",
                row=35,
                col=30,
                name="Ласишар Принц Искушения",
                faction=PieceFaction.CHAOS,
                type=PieceType.CHARACTER,
                M=9,
                T=8,
                SV=3,
                ISV=4,
                W=18,
                W_max=18,
                LD=8,
                OC=6,
                RangeWeapon=[
                    RangeWeapon(
                        name="Эмонация Боли",
                        R=20,
                        AN=6,
                        BS=2,
                        S=16,
                        AP=-4,
                        D="D6 + 3",
                        keywords=["летальные попадания", "психическое"]
                    ),
                    RangeWeapon(
                        name="Эмонация Боли (Сфокусированный Заряд)",
                        R=70,
                        AN=1,
                        BS=2,
                        S=20,
                        AP=-6,
                        D="6 + D3",
                        keywords=["психическое", "точное"]
                    ),
                    RangeWeapon(
                        name="Темный скипетер - варп разрыв",
                        R=35,
                        AN=12,
                        BS=1,
                        S=10,
                        AP=-3,
                        D="D6",
                        keywords=["психическое", "потоковое", "игнорирует укрытия"]
                    )
                ],
                MeleeWeapon=[
                    MeleeWeapon(
                        name="Спаренные блаженные клинки",
                        AN=6,
                        WS=2,
                        S=6,
                        AP=-4,
                        D="3",
                        keywords=["отравленное", "рассекающее", "спаренное"]
                    ),
                    MeleeWeapon(
                        name="Отравленные когти",
                        AN=18,
                        WS=2,
                        S=6,
                        AP=-3,
                        D="2",
                        keywords=["отравленное D3"]
                    ),
                    MeleeWeapon(
                        name="Темный скипетер - касание варпа",
                        AN=4,
                        WS=2,
                        S=20,
                        AP=-6,
                        D="6",
                        keywords=["психическое"]
                    )
                ],
                symbol="👿",
                keywords=["демон", "принц хаоса", "психик"],
                base_size=3  # Большая база для принца демонов
            ),
            GamePiece(
                id="chaos_lord",
                row=35,
                col=25,
                name="Лорд Хаоса",
                faction=PieceFaction.CHAOS,
                type=PieceType.CHARACTER,
                M=7,
                T=7,
                SV=2,
                ISV=5,
                W=12,
                W_max=12,
                LD=9,
                OC=5,
                RangeWeapon=[
                    RangeWeapon(
                        name="Болтер хаоса",
                        R=24,
                        AN=3,
                        BS=3,
                        S=4,
                        AP=-1,
                        D="1",
                        keywords=[]
                    )
                ],
                MeleeWeapon=[
                    MeleeWeapon(
                        name="Силовой меч",
                        AN=5,
                        WS=2,
                        S=5,
                        AP=-3,
                        D="2",
                        keywords=["силовое оружие"]
                    )
                ],
                symbol="💀",
                keywords=["хаос", "лорд"],
                base_size=2  # Средняя база для лорда хаоса
            ),
            # 🔵 Игрок 2 - Space Marines
            GamePiece(
                id="sm_captain",
                row=8,
                col=30,
                name="Капитан Ультрамаринов",
                faction=PieceFaction.SPACE_MARINES,
                type=PieceType.CHARACTER,
                M=7,
                T=5,
                SV=2,
                ISV=None,
                W=10,
                W_max=10,
                LD=9,
                OC=5,
                RangeWeapon=[
                    RangeWeapon(
                        name="Болтер",
                        R=24,
                        AN=3,
                        BS=2,
                        S=4,
                        AP=-1,
                        D="1",
                        keywords=[]
                    ),
                    RangeWeapon(
                        name="Грав-пистолет",
                        R=12,
                        AN=2,
                        BS=2,
                        S=5,
                        AP=-2,
                        D="2",
                        keywords=["игнорирует укрытия"]
                    )
                ],
                MeleeWeapon=[
                    MeleeWeapon(
                        name="Силовой кулак",
                        AN=4,
                        WS=2,
                        S=6,
                        AP=-3,
                        D="3",
                        keywords=["силовое оружие"]
                    )
                ],
                symbol="🛡️",
                keywords=["космодесант", "капитан", "ультрамарины"],
                base_size=2  # Средняя база для капитана
            ),
            GamePiece(
                id="sm_librarian",
                row=8,
                col=35,
                name="Либрариум",
                faction=PieceFaction.SPACE_MARINES,
                type=PieceType.CHARACTER,
                M=7,
                T=5,
                SV=2,
                ISV=5,
                W=8,
                W_max=8,
                LD=10,
                OC=4,
                RangeWeapon=[
                    RangeWeapon(
                        name="Пси-силы",
                        R=18,
                        AN=3,
                        BS=2,
                        S=8,
                        AP=-2,
                        D="D3",
                        keywords=["психическое"]
                    )
                ],
                MeleeWeapon=[
                    MeleeWeapon(
                        name="Силовой посох",
                        AN=4,
                        WS=2,
                        S=5,
                        AP=-3,
                        D="2",
                        keywords=["психическое", "силовое оружие"]
                    )
                ],
                symbol="🔮",
                keywords=["космодесант", "психик", "либрариум"],
                base_size=1  # Малая база для либриариума
            ),
        ]
        self.current_turn = PieceFaction.CHAOS

    def _get_occupied_cells(self, piece: GamePiece) -> set:
        """Получить все клетки, занимаемые моделью с учётом размера базы"""
        cells = set()
        # Для base_size=N модель занимает NxN клеток
        # Центр модели находится в (piece.row, piece.col)
        # Для нечётных баз (1, 3, 5): центр в середине клетки
        # Для чётных баз (2, 4): центр на пересечении 4 клеток
        
        if piece.base_size % 2 == 1:
            # Нечётная база (1, 3, 5) - центр в клетке
            half = piece.base_size // 2
            for dr in range(-half, half + 1):
                for dc in range(-half, half + 1):
                    cells.add((piece.row + dr, piece.col + dc))
        else:
            # Чётная база (2, 4) - центр на пересечении, занимаем клетки вокруг
            half = piece.base_size // 2
            for dr in range(-half + 1, half + 1):
                for dc in range(-half + 1, half + 1):
                    cells.add((piece.row + dr, piece.col + dc))
        return cells

    def _is_cell_occupied_by(self, row: int, col: int, exclude_piece_id: str) -> bool:
        """Проверить, занята ли клетка другой моделью (исключая указанную)"""
        for piece in self.pieces:
            if piece.id == exclude_piece_id:
                continue
            occupied = self._get_occupied_cells(piece)
            if (row, col) in occupied:
                return True
        return False

    def get_piece_at(self, row: int, col: int) -> Optional[GamePiece]:
        for piece in self.pieces:
            occupied = self._get_occupied_cells(piece)
            if (row, col) in occupied:
                return piece
        return None

    def get_pieces_by_faction(self, faction: PieceFaction) -> List[GamePiece]:
        return [p for p in self.pieces if p.faction == faction]

    def _can_place_piece_at(self, piece: GamePiece, new_row: int, new_col: int) -> bool:
        """Проверить, можно ли разместить модель в новой позиции (без коллизий и за границами)"""
        # Проверяем все клетки базы
        occupied_cells = self._get_occupied_cells_for_position(piece, new_row, new_col)
        
        for check_row, check_col in occupied_cells:
            # Проверка границ поля
            if not (0 <= check_row < self.state_rows and 0 <= check_col < self.state_cols):
                return False
            
            # Проверка коллизий с другими моделями
            if self._is_cell_occupied_by(check_row, check_col, piece.id):
                return False
        
        return True
    
    def _get_occupied_cells_for_position(self, piece: GamePiece, row: int, col: int) -> set:
        """Получить клетки, которые займёт модель в указанной позиции"""
        cells = set()
        if piece.base_size % 2 == 1:
            half = piece.base_size // 2
            for dr in range(-half, half + 1):
                for dc in range(-half, half + 1):
                    cells.add((row + dr, col + dc))
        else:
            half = piece.base_size // 2
            for dr in range(-half + 1, half + 1):
                for dc in range(-half + 1, half + 1):
                    cells.add((row + dr, col + dc))
        return cells

    def move_piece(self, piece_id: str, new_row: int, new_col: int) -> bool:
        piece = next((p for p in self.pieces if p.id == piece_id), None)
        if not piece:
            return False

        if piece.faction != self.current_turn:
            return False

        if not (0 <= new_row < self.state_rows and 0 <= new_col < self.state_cols):
            return False

        # ✅ ИСПРАВЛЕНО: Движение на основе характеристики M
        # M в WH40K это дюймы, 1 дюйм ≈ 1 клетка
        max_move = piece.M  # Теперь используем M напрямую
        distance = abs(new_row - piece.row) + abs(new_col - piece.col)

        if distance > max_move:
            return False

        # Проверка что новая позиция не занята другими моделями (с учётом размера базы)
        if not self._can_place_piece_at(piece, new_row, new_col):
            return False

        piece.row = new_row
        piece.col = new_col
        return True

    def get_valid_moves(self, piece_id: str) -> list:
        piece = next((p for p in self.pieces if p.id == piece_id), None)
        if not piece:
            return []

        if piece.faction != self.current_turn:
            return []

        moves = []
        # ✅ ИСПРАВЛЕНО: Используем M напрямую
        max_move = piece.M

        for dr in range(-max_move, max_move + 1):
            for dc in range(-max_move, max_move + 1):
                if dr == 0 and dc == 0:
                    continue
                if abs(dr) + abs(dc) > max_move:
                    continue

                new_row = piece.row + dr
                new_col = piece.col + dc

                if (0 <= new_row < self.state_rows and
                        0 <= new_col < self.state_cols and
                        self._can_place_piece_at(piece, new_row, new_col)):
                    moves.append({"row": new_row, "col": new_col})

        return moves

    def _roll_dice(self, count: int = 1) -> List[int]:
        """Бросок кубиков D6"""
        return [random.randint(1, 6) for _ in range(count)]

    def _parse_damage(self, damage_str: str) -> int:
        """Парсинг строки урона (D6, D6+3, 6, и т.д.)"""
        damage_str = damage_str.strip()

        if damage_str.isdigit():
            return int(damage_str)

        total = 0
        parts = damage_str.replace(" ", "").split("+")

        for part in parts:
            if part.startswith("D"):
                dice_count = int(part[1]) if len(part) > 1 else 1
                total += sum(self._roll_dice(dice_count))
            else:
                total += int(part)

        return total

    def _calculate_attack_success(self, attacker_skill: int, modifier: int = 0) -> bool:
        """Проверка попадания (WS или BS)"""
        roll = self._roll_dice(1)[0]
        # В WH40K: чем меньше WS/BS, тем лучше (2+ лучше чем 4+)
        target = attacker_skill + modifier
        return roll >= (7 - target) if target <= 6 else roll >= 1

    def _calculate_wound(self, strength: int, toughness: int) -> bool:
        """Проверка ранения (S vs T)"""
        ratio = strength / toughness
        if ratio >= 2:
            target = 2  # 2+
        elif ratio > 1:
            target = 3  # 3+
        elif ratio == 1:
            target = 4  # 4+
        elif ratio >= 0.5:
            target = 5  # 5+
        else:
            target = 6  # 6+

        roll = self._roll_dice(1)[0]
        return roll >= target

    def _calculate_save(self, save_value: int, ap: int, invuln_save: Optional[int] = None) -> bool:
        """Проверка спасброска"""
        modified_save = save_value + ap
        if modified_save <= 0:
            return False  # Нет спасброска

        # Используем лучший спасбросок (броня или инвалн)
        if invuln_save and invuln_save < modified_save:
            modified_save = invuln_save

        roll = self._roll_dice(1)[0]
        return roll >= modified_save

    def _calculate_distance(self, piece1: GamePiece, piece2: GamePiece) -> int:
        """Расчёт минимального расстояния между моделями с учётом размера базы"""
        # Получаем все клетки, занимаемые каждой моделью
        cells1 = self._get_occupied_cells(piece1)
        cells2 = self._get_occupied_cells(piece2)
        
        # Если клетки пересекаются - расстояние 0
        if cells1 & cells2:
            return 0
        
        # Находим минимальное расстояние между любыми двумя клетками
        min_dist = float('inf')
        for r1, c1 in cells1:
            for r2, c2 in cells2:
                dist = abs(r1 - r2) + abs(c1 - c2) - 1
                if dist < min_dist:
                    min_dist = dist
        
        return max(0, min_dist)

    def get_attack_targets(self, piece_id: str, weapon_type: str = "melee", weapon_index: int = 0) -> list:
        piece = next((p for p in self.pieces if p.id == piece_id), None)
        if not piece:
            return []

        if piece.faction != self.current_turn:
            return []

        # ✅ Выбор оружия
        if weapon_type == "range":
            if not piece.RangeWeapon or weapon_index >= len(piece.RangeWeapon):
                return []
            weapon = piece.RangeWeapon[weapon_index]
            # ✅ Конвертация: 1 дюйм = 1 клетка
            max_range = weapon.R
        else:
            if not piece.MeleeWeapon or weapon_index >= len(piece.MeleeWeapon):
                return []
            weapon = piece.MeleeWeapon[weapon_index]
            # Ближний бой = 1 клетка (от края до края)
            max_range = 1

        targets = []

        for other in self.pieces:
            if other.id == piece.id:
                continue
            if other.faction == piece.faction:
                continue

            # ✅ Расчёт дистанции с учётом размера базы
            distance = self._calculate_distance(piece, other)

            # ✅ Проверка по дальности оружия
            if distance <= max_range:
                targets.append({
                    "id": other.id,
                    "row": other.row,
                    "col": other.col,
                    "name": other.name,
                    "W": other.W,
                    "W_max": other.W_max,
                    "T": other.T,
                    "SV": other.SV,
                    "faction": other.faction,
                    "distance": distance,
                    "weapon_range": max_range
                })

        return targets

    def attack(self, attacker_id: str, defender_id: str, weapon_type: str = "melee", weapon_index: int = 0) -> dict:
        """Атака с правилами WH40K"""
        attacker = next((p for p in self.pieces if p.id == attacker_id), None)
        defender = next((p for p in self.pieces if p.id == defender_id), None)

        if not attacker or not defender:
            return {"success": False, "message": "Фишка не найдена"}

        if attacker.faction != self.current_turn:
            return {"success": False, "message": "Сейчас не ваш ход"}

        if attacker.faction == defender.faction:
            return {"success": False, "message": "Нельзя атаковать своих"}

        # ✅ Выбор оружия
        if weapon_type == "range":
            if not attacker.RangeWeapon or weapon_index >= len(attacker.RangeWeapon):
                return {"success": False, "message": "Нет дальнобойного оружия"}
            weapon = attacker.RangeWeapon[weapon_index]
            max_range = weapon.R
        else:
            if not attacker.MeleeWeapon or weapon_index >= len(attacker.MeleeWeapon):
                return {"success": False, "message": "Нет ближнего оружия"}
            weapon = attacker.MeleeWeapon[weapon_index]
            max_range = 1

        # ✅ Проверка дистанции (с учётом размера базы)
        distance = self._calculate_distance(attacker, defender)
        if distance > max_range:
            return {"success": False, "message": f"Цель вне диапазона (нужно {distance} '', доступно {max_range}'')"}

        # Расчет атаки
        total_damage = 0
        hits = 0
        wounds = 0
        failed_saves = 0

        skill = weapon.BS if weapon_type == "range" else weapon.WS

        for _ in range(weapon.AN):
            # Бросок на попадание
            if self._calculate_attack_success(skill):
                hits += 1

                # Бросок на ранение
                if self._calculate_wound(weapon.S, defender.T):
                    wounds += 1

                    # Бросок на спасбросок
                    if not self._calculate_save(defender.SV, weapon.AP, defender.ISV):
                        failed_saves += 1
                        total_damage += self._parse_damage(weapon.D)

        # Применение урона
        defender.W = max(0, defender.W - total_damage)

        attack_log = {
            "hits": hits,
            "wounds": wounds,
            "failed_saves": failed_saves,
            "total_damage": total_damage,
            "weapon_name": weapon.name,
            "weapon_type": weapon_type,
            "distance": distance,
            "weapon_range": max_range
        }

        if defender.W <= 0:
            self.pieces.remove(defender)
            return {
                "success": True,
                "message": f"{defender.name} уничтожен!",
                "killed": True,
                "attack_log": attack_log
            }

        return {
            "success": True,
            "message": f"Нанесено {total_damage} урона ({hits} попаданий, {wounds} ранений)",
            "killed": False,
            "attack_log": attack_log
        }
    def switch_turn(self) -> dict:
        if self.current_turn == PieceFaction.CHAOS:
            self.current_turn = PieceFaction.SPACE_MARINES
            return {"success": True, "current_turn": "space_marines", "message": "Ход Space Marines"}
        else:
            self.current_turn = PieceFaction.CHAOS
            return {"success": True, "current_turn": "chaos", "message": "Ход Хаоса"}

    def get_current_turn_name(self) -> str:
        names = {
            PieceFaction.CHAOS: "Хаос",
            PieceFaction.SPACE_MARINES: "Космодесант",
            PieceFaction.IMPERIUM: "Империум",
            PieceFaction.ORKS: "Орки",
        }
        return names.get(self.current_turn, self.current_turn.value)

    def reset(self):
        self._initialize_pieces()
        self.current_turn = PieceFaction.CHAOS