#include <vector>
#include <gtest/gtest.h>
#include "generated/Others.pp.hpp"
#include "util.hpp"

using namespace testing;

TEST(generated_others, ConstantTypedefEnum)
{
    std::vector<char> data(1024);

    ConstantTypedefEnum x;
    x.a[0] = 1;
    x.a[1] = 2;
    x.a[2] = 3;
    x.b = 4;
    x.c = Enum_One;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x02\x00"
            "\x03\x00\x04\x00"
            "\x01\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_others, Floats)
{
    std::vector<char> data(1024);

    Floats x;
    x.a = 10;
    x.b = 10;
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x00\x00\x20\x41" "\x00\x00\x00\x00"
            "\x00\x00\x00\x00\x00\x00\x24\x40"),
            bytes(data.data(), size));
}

TEST(generated_others, BytesFixed)
{
    std::vector<char> data(1024);

    BytesFixed x;
    x.x[0] = 'a';
    x.x[1] = 'b';
    x.x[2] = 'c';
    size_t size = x.encode(data.data());

    EXPECT_EQ(3, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "abc"),
            bytes(data.data(), size));
}

TEST(generated_others, BytesDynamic)
{
    std::vector<char> data(1024);

    BytesDynamic x;
    x.x = bytes("abcd");
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x04\x00\x00\x00"
            "abcd"),
            bytes(data.data(), size));
}

TEST(generated_others, BytesLimited)
{
    std::vector<char> data(1024);

    BytesLimited x;
    x.x = bytes("ab");
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x02\x00\x00\x00"
            "ab\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_others, BytesGreedy)
{
    std::vector<char> data(1024);

    BytesGreedy x;
    x.x = bytes("abcde");
    size_t size = x.encode(data.data());

    EXPECT_EQ(5, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "abcde"),
            bytes(data.data(), size));
}
