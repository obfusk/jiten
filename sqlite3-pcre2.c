/*
 * Written by Alexey Tourbin <at@altlinux.org>.
 * Modified by FC (Fay) Stegerman <flx@obfusk.net>.
 *
 * The author has dedicated the code to the public domain.  Anyone is free
 * to copy, modify, publish, use, compile, sell, or distribute the original
 * code, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, and by any means.
 */
#define PCRE2_CODE_UNIT_WIDTH 8
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <pcre2.h>
#include <sqlite3ext.h>
SQLITE_EXTENSION_INIT1

typedef struct {
    char *str;
    pcre2_code *code;
    pcre2_match_data *match_data;
} cache_entry;

#ifndef CACHE_SIZE
#define CACHE_SIZE 16
#endif

static void regexp(sqlite3_context *ctx, int argc, sqlite3_value **argv)
{
    const char *re, *str;
    pcre2_code *code;
    pcre2_match_data *match_data;

    assert(argc == 2);

    re = (const char *) sqlite3_value_text(argv[0]);
    if (re == NULL) {
        sqlite3_result_error(ctx, "[REGEXP] no regexp", -1);
        return;
    }

    str = (const char *) sqlite3_value_text(argv[1]);
    if (str == NULL) {
        sqlite3_result_error(ctx, "[REGEXP] no string", -1);
        return;
    }

    /* simple LRU cache */
    {
        int i;
        int found = 0;
        cache_entry *cache = sqlite3_user_data(ctx);

        assert(cache != NULL);

        for (i = 0; i < CACHE_SIZE && cache[i].str; i++) {
            if (strcmp(re, cache[i].str) == 0) {
                found = 1;
                break;
            }
        }
        if (found) {
            if (i > 0) {
                cache_entry c = cache[i];
                memmove(cache + 1, cache, i * sizeof(cache_entry));
                cache[0] = c;
            }
        }
        else {
            cache_entry c;
            int err_no;
            PCRE2_SIZE err_off;
            c.code = pcre2_compile((PCRE2_SPTR)re, PCRE2_ZERO_TERMINATED,
                                   PCRE2_UTF | PCRE2_UCP, &err_no, &err_off, NULL);
            if (c.code == NULL) {
                PCRE2_UCHAR err[256];
                pcre2_get_error_message(err_no, err, sizeof(err));
                char *e = sqlite3_mprintf("[REGEXP] %s: %s (offset %d)", re, err, err_off);
                sqlite3_result_error(ctx, e, -1);
                sqlite3_free(e);
                return;
            }
            c.match_data = pcre2_match_data_create_from_pattern(c.code, NULL);
            if (c.match_data == NULL) {
                sqlite3_result_error(ctx, "[REGEXP] pcre2_match_data_create_from_pattern: ENOMEM", -1);
                pcre2_code_free(c.code);
                return;
            }
            c.str = strdup(re);
            if (c.str == NULL) {
                sqlite3_result_error(ctx, "[REGEXP] strdup: ENOMEM", -1);
                pcre2_match_data_free(c.match_data);
                pcre2_code_free(c.code);
                return;
            }
            i = CACHE_SIZE - 1;
            if (cache[i].str) {
                free(cache[i].str);
                assert(cache[i].code != NULL);
                pcre2_match_data_free(cache[i].match_data);
                pcre2_code_free(cache[i].code);
            }
            memmove(cache + 1, cache, i * sizeof(cache_entry));
            cache[0] = c;
        }
        code = cache[0].code;
        match_data = cache[0].match_data;
    }

    {
        int rc;
        assert(code != NULL);
        rc = pcre2_match(code, (PCRE2_SPTR)str, PCRE2_ZERO_TERMINATED, 0, 0, match_data, NULL);
        sqlite3_result_int(ctx, rc >= 0);
        return;
    }
}

int sqlite3_extension_init(sqlite3 *db, char **err, const sqlite3_api_routines *api)
{
    SQLITE_EXTENSION_INIT2(api)
    cache_entry *cache = calloc(CACHE_SIZE, sizeof(cache_entry));
    if (cache == NULL) {
        *err = "[REGEXP] calloc: ENOMEM";
        return 1;
    }
    sqlite3_create_function(db, "REGEXP", 2, SQLITE_UTF8, cache, regexp, NULL, NULL);
    return 0;
}
