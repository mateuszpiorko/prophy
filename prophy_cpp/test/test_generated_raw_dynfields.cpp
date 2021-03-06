#include <gtest/gtest.h>
#include "util.hpp"
#include "generated_raw/Dynfields.pp.hpp"

using namespace testing;

TEST(generated_raw_dynfields, Dynfields)
{
    test_swap<Dynfields>(
        "\x00\x00\x00\x05"
        "\x01\x02\x03\x04"
        "\x05\xab"
        "\x00\x02\x00\x01"
        "\x00\x02"
        "\x03\xab\xab\xab\xab\xab\xab\xab"
        "\x00\x00\x00\x00\x00\x00\x00\x01"
        "\x00\x00\x00\x00\x00\x00\x00\x02"
        "\x00\x00\x00\x00\x00\x00\x00\x03",

        "\x05\x00\x00\x00"
        "\x01\x02\x03\x04"
        "\x05\xab"
        "\x02\x00\x01\x00"
        "\x02\x00"
        "\x03\xab\xab\xab\xab\xab\xab\xab"
        "\x01\x00\x00\x00\x00\x00\x00\x00"
        "\x02\x00\x00\x00\x00\x00\x00\x00"
        "\x03\x00\x00\x00\x00\x00\x00\x00"
    );
}

TEST(generated_raw_dynfields, DynfieldsMixed)
{
    test_swap<DynfieldsMixed>(
        "\x00\x00\x00\x05"
        "\x00\x02"
        "\x01\x02\x03\x04"
        "\x05\x00"
        "\x00\x01\x00\x02",

        "\x05\x00\x00\x00"
        "\x02\x00"
        "\x01\x02\x03\x04"
        "\x05\x00"
        "\x01\x00\x02\x00"
    );
}

TEST(generated_raw_dynfields, DynfieldsOverlapped)
{
    test_swap<DynfieldsOverlapped>(
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x03"
        "\x00\x01\x00\x02"
        "\x00\x03\xab\xcd"
        "\x00\x00\x00\x05"
        "\x00\x04\x00\x05"
        "\x00\x06\x00\x07"
        "\x00\x08\xab\xcd"
        "\x00\x09\xab\xcd",

        "\x01\x00\x00\x00"
        "\x03\x00\x00\x00"
        "\x01\x00\x02\x00"
        "\x03\x00\xab\xcd"
        "\x05\x00\x00\x00"
        "\x04\x00\x05\x00"
        "\x06\x00\x07\x00"
        "\x08\x00\xab\xcd"
        "\x09\x00\xab\xcd"
    );
}

TEST(generated_raw_dynfields, DynfieldsPadded)
{
    test_swap<DynfieldsPadded>(
        "\x01\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x02\x02\x03\x00"
        "\x00\x00\x00\x02"
        "\x04\x05\x00\x00"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x06",

        "\x01\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x02\x02\x03\x00"
        "\x02\x00\x00\x00"
        "\x04\x05\x00\x00"
        "\x00\x00\x00\x00"
        "\x06\x00\x00\x00"
        "\x00\x00\x00\x00"
    );
}

TEST(generated_raw_dynfields, DynfieldsFixtail)
{
    test_swap<DynfieldsFixtail>(
        "\x02\x02\x03\x00"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x04"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x05",

        "\x02\x02\x03\x00"
        "\x00\x00\x00\x00"
        "\x04\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x05\x00\x00\x00"
        "\x00\x00\x00\x00"
    );
}

TEST(generated_raw_dynfields, DynfieldsComp)
{
    test_swap<DynfieldsComp>(
        "\x00\x00\x00\x01"
        "\x00\x01\xab\xcd"
        "\x00\x00\x00\x02"
        "\x00\x02\x00\x03"
        "\x00\x00\x00\x03"
        "\x00\x04\x00\x05"
        "\x00\x06\xab\xcd",

        "\x01\x00\x00\x00"
        "\x01\x00\xab\xcd"
        "\x02\x00\x00\x00"
        "\x02\x00\x03\x00"
        "\x03\x00\x00\x00"
        "\x04\x00\x05\x00"
        "\x06\x00\xab\xcd"
    );
}
