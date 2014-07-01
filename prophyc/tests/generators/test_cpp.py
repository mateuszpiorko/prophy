from prophyc import model
from prophyc.generators.cpp import CppGenerator

def generate(nodes):
    return CppGenerator().generate_definitions(nodes)

def generate_full(nodes, basename):
    return CppGenerator().serialize_string(nodes, basename)

def test_generate_includes():
    nodes = [model.Include("szydlo"),
             model.Include("mydlo"),
             model.Include("powidlo")]

    assert generate(nodes) == """\
#include "szydlo.hpp"
#include "mydlo.hpp"
#include "powidlo.hpp"
"""

def test_generate_constants():
    nodes = [model.Constant("CONST_A", "0"),
             model.Constant("CONST_B", "31")]

    assert generate(nodes) == """\
enum { CONST_A = 0 };
enum { CONST_B = 31 };
"""

def test_generate_typedefs():
    nodes = [model.Typedef("a", "b")]

    assert generate(nodes) == """\
typedef b a;
"""

def test_generate_enums():
    nodes = [model.Enum("EEnum", [model.EnumMember("EEnum_A", "0"),
                                  model.EnumMember("EEnum_B", "1"),
                                  model.EnumMember("EEnum_C", "2")])]

    assert generate(nodes) == """\
enum EEnum
{
    EEnum_A = 0,
    EEnum_B = 1,
    EEnum_C = 2
};
"""

def test_generate_struct():
    nodes = [model.Struct("Struct", [(model.StructMember("a", "u8", None, None, None, False)),
                                     (model.StructMember("b", "i64", None, None, None, False)),
                                     (model.StructMember("c", "r32", None, None, None, False)),
                                     (model.StructMember("d", "TTypeX", None, None, None, False))])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a;
    int64_t b;
    float c;
    TTypeX d;
};
"""

def test_generate_struct_with_dynamic_array():
    nodes = [model.Struct("Struct", [model.StructMember("tmpName", "TNumberOfItems", None, None, None, False),
                                     model.StructMember("a", "u8", True, "tmpName", None, False)])]

    assert generate(nodes) == """\
struct Struct
{
    TNumberOfItems tmpName;
    uint8_t a[1]; /// dynamic array, size in tmpName
};
"""

def test_generate_struct_with_fixed_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u8", True, None, "NUM_OF_ARRAY_ELEMS", False)])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a[NUM_OF_ARRAY_ELEMS];
};
"""

def test_generate_struct_with_limited_array():
    nodes = [model.Struct("Struct", [model.StructMember("a_len", "u8", None, None, None, False),
                                     model.StructMember("a", "u8", True, "a_len", "NUM_OF_ARRAY_ELEMS", False)])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a_len;
    uint8_t a[NUM_OF_ARRAY_ELEMS]; /// limited array, size in a_len
};
"""

def test_generate_struct_with_byte():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", False, None, None, None)])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a;
};
"""

def test_generate_struct_with_byte_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", True, None, None, None)])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a[1]; /// greedy array
};
"""

def test_generate_struct_many_arrays():
    nodes = [
        model.Struct("ManyArrays", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False),
            model.StructMember("num_of_b", "u8", None, None, None, False),
            model.StructMember("b", "u8", True, "num_of_b", None, False),
            model.StructMember("num_of_c", "u8", None, None, None, False),
            model.StructMember("c", "u8", True, "num_of_c", None, False)
        ])
    ]

    assert generate(nodes) == """\
struct ManyArrays
{
    uint8_t num_of_a;
    uint8_t a[1]; /// dynamic array, size in num_of_a

    struct part2
    {
        uint8_t num_of_b;
        uint8_t b[1]; /// dynamic array, size in num_of_b
    } _2;

    struct part3
    {
        uint8_t num_of_c;
        uint8_t c[1]; /// dynamic array, size in num_of_c
    } _3;
};
"""

def test_generate_struct_many_arrays_mixed():
    nodes = [
        model.Struct("ManyArraysMixed", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("num_of_b", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False),
            model.StructMember("b", "u8", True, "num_of_b", None, False)
        ])
    ]

    assert generate(nodes) == """\
struct ManyArraysMixed
{
    uint8_t num_of_a;
    uint8_t num_of_b;
    uint8_t a[1]; /// dynamic array, size in num_of_a

    struct part2
    {
        uint8_t b[1]; /// dynamic array, size in num_of_b
    } _2;
};
"""

def test_generate_struct_with_dynamic_fields():
    nodes = [
        model.Struct("Dynamic", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False)
        ]),
        model.Struct("X", [
            model.StructMember("a", "u8", None, None, None, False),
            model.StructMember("b", "Dynamic", None, None, None, False),
            model.StructMember("c", "u8", None, None, None, False)
        ])
    ]

    assert generate(nodes) == """\
struct Dynamic
{
    uint8_t num_of_a;
    uint8_t a[1]; /// dynamic array, size in num_of_a
};

struct X
{
    uint8_t a;
    Dynamic b;

    struct part2
    {
        uint8_t c;
    } _2;
};
"""

def test_generate_newlines():
    nodes = [model.Typedef("a", "b"),
             model.Typedef("c", "d"),
             model.Enum("E1", [model.EnumMember("E1_A", "0")]),
             model.Enum("E2", [model.EnumMember("E2_A", "0")]),
             model.Constant("CONST_A", "0"),
             model.Typedef("e", "f"),
             model.Constant("CONST_B", "0"),
             model.Constant("CONST_C", "0"),
             model.Struct("A", [model.StructMember("a", "u32", False, None, None, None)]),
             model.Struct("B", [model.StructMember("b", "u32", False, None, None, None)])]

    assert generate(nodes) == """\
typedef b a;
typedef d c;

enum E1
{
    E1_A = 0
};

enum E2
{
    E2_A = 0
};

enum { CONST_A = 0 };

typedef f e;

enum { CONST_B = 0 };
enum { CONST_C = 0 };

struct A
{
    uint32_t a;
};

struct B
{
    uint32_t b;
};
"""

def test_generate_struct():
    nodes = [
        model.Struct("Struct", [
            (model.StructMember("a", "u8", None, None, None, False))
        ])
    ]

    assert generate_full(nodes, "TestFile") == """\
#ifndef _PROPHY_GENERATED_TestFile_HPP
#define _PROPHY_GENERATED_TestFile_HPP

#include <prophy/prophy.hpp>

struct Struct
{
    uint8_t a;
};

#endif  /* _PROPHY_GENERATED_TestFile_HPP */
"""