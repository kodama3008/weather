#include <stdio.h>
#include <string.h>

/* --- 定数定義 ---------------------------------------------------- */
#define MAX_ROOMS   5
#define MAX_ITEMS   3
#define INVENTORY  -1          /* プレイヤー所持中を示す値 */

/* --- 構造体定義 -------------------------------------------------- */
typedef struct Room {
    const char *name;
    const char *desc;
    int n, s, e, w;            /* 隣接部屋インデックス (-1 は行き止まり) */
} Room;

typedef struct Item {
    const char *name;          /* アイテム名（1語想定） */
    int  location;             /* 置き場所: 部屋ID か INVENTORY */
} Item;

/* --- マップ定義 -------------------------------------------------- */
Room rooms[MAX_ROOMS] = {
    /* name,        desc,                        N  S  E  W */
    {"Entrance",   "薄暗い洞窟の入口だ。",        1,-1,-1,-1},
    {"Hallway",    "長い通路が続いている。",      2, 0, 3,-1},
    {"Treasure",   "部屋の中央に宝箱がある!",    -1, 1,-1,-1},
    {"Armory",     "錆びた武器が壁に掛かる。",   -1,-1,-1, 1},
    {"Trap Room",  "床が抜けそうで危険だ!",     -1,-1,-1,-1}
};

/* --- アイテム初期配置 -------------------------------------------- */
Item items[MAX_ITEMS] = {
    {"Key",   2},   /* Treasure に落ちている */
    {"Sword", 3},   /* Armory   に落ちている */
    {"Gem",   4}    /* Trap Room に落ちている */
};

/* --- ヘルパ関数 -------------------------------------------------- */
void show_room(int id)
{
    printf("\n== %s ==\n%s\n", rooms[id].name, rooms[id].desc);

    /* 落ちているアイテムの表示 */
    for (int i = 0; i < MAX_ITEMS; ++i) {
        if (items[i].location == id)
            printf("[ここに %s がある]\n", items[i].name);
    }

    /* 出口一覧 */
    printf("出口: ");
    if (rooms[id].n != -1) printf("north ");
    if (rooms[id].s != -1) printf("south ");
    if (rooms[id].e != -1) printf("east ");
    if (rooms[id].w != -1) printf("west ");
    printf("\n> ");
}

/* --- メイン ------------------------------------------------------ */
int main(void)
{
    char buf[128], verb[16], obj[32];
    int here = 0;          /* 現在地 (Entrance) */
    int running = 1;

    puts("Welcome to Mini-Zork!  Type 'help' for commands.");
    show_room(here);

    while (running && fgets(buf, sizeof buf, stdin)) {
        verb[0] = obj[0] = '\0';
        sscanf(buf, "%15s %31s", verb, obj);   /* 動詞と目的語を抽出 */

        /* --- 移動 ------------------------------------------------ */
        if (strcmp(verb, "go") == 0) {
            int next = -1;
            if      (strcmp(obj, "north") == 0) next = rooms[here].n;
            else if (strcmp(obj, "south") == 0) next = rooms[here].s;
            else if (strcmp(obj, "east")  == 0) next = rooms[here].e;
            else if (strcmp(obj, "west")  == 0) next = rooms[here].w;

            if (next != -1) {
                here = next;
                show_room(here);
            } else {
                puts("その方向には道がない。\n> ");
            }
        }

        /* --- 観察 ------------------------------------------------ */
        else if (strcmp(verb, "look") == 0) {
            show_room(here);
        }

        /* --- アイテム取得 ---------------------------------------- */
        else if (strcmp(verb, "take") == 0) {
            int found = 0;
            for (int i = 0; i < MAX_ITEMS; ++i) {
                if (items[i].location == here &&
                    strcmp(items[i].name, obj) == 0)
                {
                    items[i].location = INVENTORY;
                    printf("%s を手に入れた！\n> ", items[i].name);
                    found = 1;
                    break;
                }
            }
            if (!found) puts("ここにはそのアイテムはない。\n> ");
        }

        /* --- 所持品表示 ------------------------------------------ */
        else if (strcmp(verb, "inventory") == 0 ||
                 strcmp(verb, "inv") == 0)
        {
            puts("【持ち物】");
            int empty = 1;
            for (int i = 0; i < MAX_ITEMS; ++i) {
                if (items[i].location == INVENTORY) {
                    printf(" - %s\n", items[i].name);
                    empty = 0;
                }
            }
            if (empty) puts(" (何も持っていない)");
            printf("> ");
        }

        /* --- ヘルプ ---------------------------------------------- */
        else if (strcmp(verb, "help") == 0) {
            puts("コマンド: "
                 "go <north|south|east|west>, "
                 "look, "
                 "take <item>, "
                 "inventory (inv), "
                 "quit\n> ");
        }

        /* --- 終了 ------------------------------------------------ */
        else if (strcmp(verb, "quit") == 0) {
            running = 0;
        }

        /* --- 不明コマンド ---------------------------------------- */
        else {
            puts("知らないコマンドだ。'help' を参照。\n> ");
        }
    }

    puts("Bye!");
    return 0;
}
