from WII_Config import *

def converter(rtl, rtr, rbl, rbr):
    [converted_tl, converted_tr, converted_bl, converted_br] = all_2_kilo([rtl, rtr, rbl, rbr],
                                                                          [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT,
                                                                           BOTTOM_RIGHT],
                                                                          calibration_matrix_adjusted)

    [converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a] = all_2_converting([converted_tl, converted_tr,
                                                                                         converted_bl, converted_br],
                                                                                        [TOP_LEFT, TOP_RIGHT,
                                                                                         BOTTOM_LEFT, BOTTOM_RIGHT])
    return [converted_tl_a, converted_tr_a, converted_bl_a, converted_br_a]

def raw_to_kilos(raw_data_point, corner, matrix):
    converted = []

    x_0_17 = matrix[0][corner] * 1.0
    y_0_17 = 0.0

    x_1_17 = matrix[1][corner] * 1.0
    y_1_17 = 17.0

    x_0_37 = x_1_17
    y_0_37 = y_1_17

    x_1_37 = matrix[2][corner] * 1.0
    y_1_37 = 37.5

    cte_17 = ((x_1_17 * y_0_17 - x_0_17 * y_1_17) / (x_1_17 - x_0_17))

    cte_37 = ((x_1_37 * y_0_37 - x_0_37 * y_1_37) / (x_1_37 - x_0_37))

    # m_17 = (17*1.0) / (matrix[1][corner] - matrix[0][corner]*1.0)
    # b_17 = 17 - m_17 * matrix[1][corner] * 1.0

    # m_37 = (37.5 * 1.0 - 17.0) / (matrix[2][corner] - matrix[1][corner] * 1.0)
    # b_37 = 37.5 - m_37 * matrix[2][corner] * 1.0

    for i in range(0, len(raw_data_point)):

        if raw_data_point[i] <= matrix[1][corner]:
            value = raw_data_point[i] * ((y_1_17 - y_0_17) / (x_1_17 - x_0_17)) + cte_17
        else:
            value = raw_data_point[i] * ((y_1_37 - y_0_37) / (x_1_37 - x_0_37)) + cte_37

        if value < 0:
            value = 0
        converted.append(value)
    return converted


def all_2_kilo(raw_vectors, corners, matrix):
    output = []

    for i in range(0, len(raw_vectors)):
        output.append(raw_to_kilos(raw_vectors[i], corners[i], matrix))
    return output


def scaler(kg_vector, corner):
    x_0_17 = 0
    y_0_17 = 0.0

    x_1_17 = Scale_16[4]
    y_1_17 = Scale_16[corner] * 1.0

    x_0_37 = x_1_17
    y_0_37 = y_1_17

    x_1_37 = Scale_25[4]
    y_1_37 = Scale_25[corner] * 1.0

    cte_17 = ((x_1_17 * y_0_17 - x_0_17 * y_1_17) / (x_1_17 - x_0_17))

    cte_37 = ((x_1_37 * y_0_37 - x_0_37 * y_1_37) / (x_1_37 - x_0_37))

    converted = []

    for i in range(0, len(kg_vector)):

        if kg_vector[i] <= Scale_16[4]:
            value = kg_vector[i] + kg_vector[i] * ((y_1_17 - y_0_17) / (x_1_17 - x_0_17)) + cte_17
        else:
            value = kg_vector[i] + kg_vector[i] * ((y_1_37 - y_0_37) / (x_1_37 - x_0_37)) + cte_37

        if value < 0:
            value = 0
        converted.append(value)
    return converted


def all_2_converting(raw_vectors, corners):
    output = []
    for i in range(0, len(raw_vectors)):
        output.append(scaler(raw_vectors[i], corners[i]))
    return output
