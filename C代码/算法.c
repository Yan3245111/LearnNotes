// 二分法
uint8_t part_21(uint8_t start, uint8_t end, uint8_t res, uint8_t list[]) {
    uint8_t mid = (start + end) / 2;
    if (res == list[mid]) {
        return mid;
    }
    else if (res < list[mid]) {
        return part_21(start, mid - 1, res, list);
    }
    else if (res > list[mid]) {
        return part_21(mid + 1, end, res, list);
    }
}

void part_2(void) {
    uint8_t list_array[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18};
    uint8_t num = 5;
    uint8_t res = part_21(list_array[0], list_array[17], num, list_array);
    printf("%d\n", res);
}
