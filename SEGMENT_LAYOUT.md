# H617E Segment Numbering & Layout

```
Light Strip Layout (H617E RGBIC - 15 Segments)

Segment Index:   0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
Display Number:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15

Visual Layout:
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│ 01 │ 02 │ 03 │ 04 │ 05 │ 06 │ 07 │ 08 │ 09 │ 10 │ 11 │ 12 │ 13 │ 14 │ 15 │
└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
  0    1    2    3    4    5    6    7    8    9   10   11   12   13   14
```

## Entity Naming

Each segment is accessible through Home Assistant as a light entity:

| Segment # | Entity ID                        | Index | Note |
|-----------|----------------------------------|-------|------|
| 1         | light.govee_h617e_segment_0    | 0     | Leftmost segment |
| 2         | light.govee_h617e_segment_1    | 1     | |
| 3         | light.govee_h617e_segment_2    | 2     | |
| 4         | light.govee_h617e_segment_3    | 3     | |
| 5         | light.govee_h617e_segment_4    | 4     | |
| 6         | light.govee_h617e_segment_5    | 5     | Middle-left segment |
| 7         | light.govee_h617e_segment_6    | 6     | |
| 8         | light.govee_h617e_segment_7    | 7     | Center segment |
| 9         | light.govee_h617e_segment_8    | 8     | |
| 10        | light.govee_h617e_segment_9    | 9     | Middle-right segment |
| 11        | light.govee_h617e_segment_10   | 10    | |
| 12        | light.govee_h617e_segment_11   | 11    | |
| 13        | light.govee_h617e_segment_12   | 12    | |
| 14        | light.govee_h617e_segment_13   | 13    | |
| 15        | light.govee_h617e_segment_14   | 14    | Rightmost segment |

## Common Usage Patterns

### Group All Segments
If you want to control all segments together, you can create a Light Group in Home Assistant:

```yaml
# groups.yaml
light_h617e_all_segments:
  name: "H617E All Segments"
  entities:
    - light.govee_h617e_segment_0
    - light.govee_h617e_segment_1
    - light.govee_h617e_segment_2
    - light.govee_h617e_segment_3
    - light.govee_h617e_segment_4
    - light.govee_h617e_segment_5
    - light.govee_h617e_segment_6
    - light.govee_h617e_segment_7
    - light.govee_h617e_segment_8
    - light.govee_h617e_segment_9
    - light.govee_h617e_segment_10
    - light.govee_h617e_segment_11
    - light.govee_h617e_segment_12
    - light.govee_h617e_segment_13
    - light.govee_h617e_segment_14
```

### Groups by Position
Group segments by physical position for easier reference:

```yaml
# groups.yaml
light_h617e_left_half:
  name: "H617E Left Segments (1-7)"
  entities:
    - light.govee_h617e_segment_0
    - light.govee_h617e_segment_1
    - light.govee_h617e_segment_2
    - light.govee_h617e_segment_3
    - light.govee_h617e_segment_4
    - light.govee_h617e_segment_5
    - light.govee_h617e_segment_6

light_h617e_right_half:
  name: "H617E Right Segments (8-15)"
  entities:
    - light.govee_h617e_segment_7
    - light.govee_h617e_segment_8
    - light.govee_h617e_segment_9
    - light.govee_h617e_segment_10
    - light.govee_h617e_segment_11
    - light.govee_h617e_segment_12
    - light.govee_h617e_segment_13
    - light.govee_h617e_segment_14
```

### Groups by Quarter
Divide segments into quadrants:

```yaml
# groups.yaml
light_h617e_quarter_1:
  name: "H617E Quarter 1 (1-4)"
  entities:
    - light.govee_h617e_segment_0
    - light.govee_h617e_segment_1
    - light.govee_h617e_segment_2
    - light.govee_h617e_segment_3

light_h617e_quarter_2:
  name: "H617E Quarter 2 (5-8)"
  entities:
    - light.govee_h617e_segment_4
    - light.govee_h617e_segment_5
    - light.govee_h617e_segment_6
    - light.govee_h617e_segment_7

light_h617e_quarter_3:
  name: "H617E Quarter 3 (9-12)"
  entities:
    - light.govee_h617e_segment_8
    - light.govee_h617e_segment_9
    - light.govee_h617e_segment_10
    - light.govee_h617e_segment_11

light_h617e_quarter_4:
  name: "H617E Quarter 4 (13-15)"
  entities:
    - light.govee_h617e_segment_12
    - light.govee_h617e_segment_13
    - light.govee_h617e_segment_14
```

## Color Reference

Here are some common RGB colors you can use:

| Color | RGB | Hex |
|-------|-----|-----|
| Red | [255, 0, 0] | #FF0000 |
| Green | [0, 255, 0] | #00FF00 |
| Blue | [0, 0, 255] | #0000FF |
| White | [255, 255, 255] | #FFFFFF |
| Yellow | [255, 255, 0] | #FFFF00 |
| Cyan | [0, 255, 255] | #00FFFF |
| Magenta | [255, 0, 255] | #FF00FF |
| Orange | [255, 165, 0] | #FFA500 |
| Purple | [128, 0, 128] | #800080 |
| Pink | [255, 192, 203] | #FFC0CB |
| Black | [0, 0, 0] | #000000 |
