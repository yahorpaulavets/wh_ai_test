from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.models import MoveRequest, AttackRequestWH
from src.game_service import GameService
from pathlib import Path
import uvicorn

app = FastAPI(title="Warhammer 40K Battle Field")
game_service = GameService()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

if not STATIC_DIR.exists():
    STATIC_DIR = Path(__file__).resolve().parent / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/game/state")
async def get_game_state():
    return {
        "rows": game_service.state_rows,
        "cols": game_service.state_cols,
        "pieces": [piece.model_dump() for piece in game_service.pieces]
    }


@app.get("/api/game/turn")
async def get_current_turn():
    return {
        "current_turn": game_service.current_turn.value,
        "current_player": game_service.get_current_turn_name()
    }


@app.post("/api/game/switch-turn")
async def switch_turn():
    result = game_service.switch_turn()
    return result


@app.get("/api/game/piece/{piece_id}")
async def get_piece(piece_id: str):
    piece = next((p for p in game_service.pieces if p.id == piece_id), None)
    if not piece:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    return piece.model_dump()


@app.get("/api/game/piece/{piece_id}/moves")
async def get_valid_moves(piece_id: str):
    return {"moves": game_service.get_valid_moves(piece_id)}


@app.get("/api/game/piece/{piece_id}/targets")
async def get_attack_targets(piece_id: str, weapon_type: str = "melee"):
    return {"targets": game_service.get_attack_targets(piece_id, weapon_type)}


@app.post("/api/game/move")
async def move_piece(request: MoveRequest):
    success = game_service.move_piece(request.piece_id, request.new_row, request.new_col)
    if not success:
        raise HTTPException(status_code=400, detail="Недопустимый ход")
    return {"success": True, "message": "Персонаж перемещён"}


@app.post("/api/game/attack")
async def attack(request: AttackRequestWH):
    result = game_service.attack(
        request.attacker_id,
        request.defender_id,
        request.weapon_type,
        request.weapon_index
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/api/game/reset")
async def reset_game():
    game_service.reset()
    return {"success": True, "message": "Игра сброшена"}


@app.get("/api/game/piece/{piece_id}/targets")
async def get_attack_targets(
    piece_id: str,
    weapon_type: str = "melee",
    weapon_index: int = 0
):
    return {"targets": game_service.get_attack_targets(piece_id, weapon_type, weapon_index)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.1.140", port=80, reload=True)
