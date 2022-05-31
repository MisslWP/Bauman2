/**
 * \file main.c
 * \brief Разместить сумму цифр числа после каждого числа, являющегося простым в введённом массиве.
 */

#include <stdio.h>
#include <assert.h>

#define ERR_IO 1
#define ERR_SIZE 2
#define ERR_TEST 3
#define OK 0
#define INP_ERR -1
#define SIZE_ERR -1
#define NULL_ARR_ERR -2
#define NULL_FILE_ERR -3
#define PRIME 1
#define NOT_PRIME 0

/**
 * \def N
 * \brief Максимальный размер массива
 */
#define N 100

int print_array(int *arr, int size, FILE *stream);
int input_array(int *arr, int size);
int digit_sum(int num);
int is_prime(int n);
int test_is_prime();
int test_digit_sum();
int test_print_array();

/**
 * \fn int main(void)
 * \brief Точка входа в программу
 * \return Код ошибки
 */
int main(void)
{
    assert(test_is_prime() == 0);
    assert(test_digit_sum() == 0);
    assert(test_print_array() == 0);

    int n, return_code = OK;

    printf("Please, input n: ");
    if (scanf("%d", &n) != 1)
    {
        printf("Invalid input!\n");
        return_code = ERR_IO;
    }
    else if (n < 1 || n > N)
    {
        printf("Invalid n! N must be more than zero and more or equal to one hundred!\n");
        return_code = ERR_SIZE;
    }
    else
    {
        int arr[N];
        printf("Please, input array: ");
        if (input_array(arr, n) != OK)
        {
            printf("Invalid input!\n");
            return_code = ERR_IO;
        }
        else
        {
            int new_arr[2*N];
            int new_size = 0;
            for (int i = 0; i < n; i++)
            {
                int cur = arr[i];
                new_arr[new_size++] = cur;
                if (is_prime(cur))
                    new_arr[new_size++] = digit_sum(cur);
            }
            print_array(new_arr, new_size, stdout);
        }
    }

    return return_code;
}

/**
 * \fn int test_is_prime()
 * \brief Модульный тест для функции \link is_prime(int n)
 *
 * \return Количество проваленных тестов
 */
int test_is_prime()
{
    int err_count = 0;

    // Числа, не являющиеся простыми
    {
        // Неположительные числа
        err_count += is_prime(-3) == NOT_PRIME ? 0 : 1;
        err_count += is_prime(0) == NOT_PRIME ? 0 : 1;
        // Единица (краевой случай)
        err_count += is_prime(1) == NOT_PRIME ? 0 : 1;

        // Некоторые другие числа
        err_count += is_prime(4) == NOT_PRIME ? 0 : 1;
        err_count += is_prime(18) == NOT_PRIME ? 0 : 1;
        err_count += is_prime(9) == NOT_PRIME ? 0 : 1;
    }

    // Числа, являющиеся простыми
    {
        err_count += is_prime(2) == PRIME ? 0 : 1;
        err_count += is_prime(3) == PRIME ? 0 : 1;
        err_count += is_prime(5) == PRIME ? 0 : 1;
        err_count += is_prime(7) == PRIME ? 0 : 1;
        err_count += is_prime(17) == PRIME ? 0 : 1;
        err_count += is_prime(499) == PRIME ? 0 : 1;
    }

    return err_count;
}

/**
 * \fn int test_digit_sum()
 * \brief Модульный тест для функции \link digit_sum(int num) \endlink
 *
 * \return Количество проваленных тестов
 */
int test_digit_sum()
{
    int err_count = 0;

    // Отрицательные числа
    err_count += digit_sum(-153) == 9 ? 0 : 1;
    err_count += digit_sum(-1) == 1 ? 0 : 1;
    err_count += digit_sum(-999) == 27 ? 0 : 1;

    // Ноль
    err_count += digit_sum(0) == 0 ? 0 : 1;

    // Положительные числа
    err_count += digit_sum(1) == 1 ? 0 : 1;
    err_count += digit_sum(19) == 10 ? 0 : 1;
    err_count += digit_sum(10001) == 2 ? 0 : 1;

    return err_count;
}

/**
 * \fn int test_print_array()
 * \brief Модульный тест для функции \link print_array(int *arr, int size, FILE *stream) \endlink
 *
 * \return Количество проваленных тестов
 */
int test_print_array()
{
    int err_count = 0;

    FILE *null;

    null = fopen("/dev/null", "w");

    // Массив - NULL
    {
        int *arr = NULL;
        err_count += print_array(arr, 1, null) == NULL_ARR_ERR ? 0 : 1;
    }
    // Массив не содержит данных
    {
        int arr[] = {1, 2, 3, 4, 5};
        err_count += print_array(arr, -1, null) == SIZE_ERR ? 0 : 1;
        err_count += print_array(arr, -17, null) == SIZE_ERR ? 0 : 1;
        err_count += print_array(arr, 0, null) == SIZE_ERR ? 0 : 1;
    }

    // Корректный массив
    {
        int arr[] = {-4, -3, 5, 7, 0};
        err_count += print_array(arr, 5, null) == OK ? 0 : 1;
    }

    // Корректный массив, но файл - NULL
    {
        int arr[] = {-4, -3, 5, 7, 0};
        err_count += print_array(arr, 1, NULL) == NULL_FILE_ERR ? 0 : 1;
        err_count += print_array(arr, 3, NULL) == NULL_FILE_ERR ? 0 : 1;
    }

    fclose(null);

    return err_count;
}

/**
 * \fn int digit_sum(int num)
 * \brief Подсчитывает сумму цифр числа
 *
 *
 * \param [in] num Число, для которого необходимо посчитать сумму цифр
 * \return Сумма цифр числа
 */
int digit_sum(int num)
{
    if (num < 0)
        num = -num;
    int sum = 0;
    while (num != 0)
    {
        sum += num % 10;
        num /= 10;
    }
    return sum;
}

/**
 * \fn int is_prime(int n)
 * \brief Проверяет, является ли число простым
 *
 * \param [in] n Число для проверки
 * \return Является ли число простым
 */
int is_prime(int n)
{
    int return_code = PRIME;
    /// Числа меньше двух - не простые
    if (n < 2)
    {
        return_code = NOT_PRIME;
    }
    else
    {
        for (int i = 2; (i <= n / 2) && (return_code == PRIME); i++)
        {
            if (n % i == 0)
                return_code = NOT_PRIME;
        }
    }

    return return_code;
}

/**
 * \fn void print_array(int *arr, int size, FILE *stream)
 * \brief Выводит первые size элементов массива в заданный поток
 *
 * \param [in] arr Массив, который необходимо вывести
 * \param [in] size Колчество выводимых элементов массива
 * \param [in] stream Поток, в который происходит вывод массива
 *
 * \return Код ошибки
 */
int print_array(int *arr, int size, FILE *stream)
{
    int rc = OK;
    if (stream != NULL)
    {
        if (arr != NULL)
        {
            if (size > 0)
            {
                for (int i = 0; i < size; i++)
                {
                    fprintf(stream, "%d", arr[i]);
                    if (i != size - 1)
                        fprintf(stream, " ");
                }
                fprintf(stream, "\n");
            }
            else
            {
                rc = SIZE_ERR;
            }
        }
        else
        {
            rc = NULL_ARR_ERR;
        }
    }
    else
    {
        rc = NULL_FILE_ERR;
    }

    return rc;
}

/**
 * \fn int input_array(int *arr, int size)
 * \brief Ввод массива
 *
 * \param [out] arr Вводимый массив
 * \param [in] size Размер массива
 * \return Код ошибки
 */
int input_array(int *arr, int size)
{
    int state = OK;
    for (int i = 0; i < size && ((state = (scanf("%d", arr + i)) == 1 ? OK : INP_ERR) == OK); i++);
    return state;
}
