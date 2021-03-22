# from AccelerometerInputSource import MPUInputSource
from MockInputSource import MockInputSource
from LiveInputSource import LiveInputSource


def get_input_sources(mpu1_source, mpu2_source, received_new_mpu1_reading, received_new_mpu2_reading):

    if mpu1_source == "MPU1" and mpu2_source == "MPU2":
        print("\n# MPU1 and MPU2 source ...")
        # input1_source = MPUInputSource(0b00000001, received_new_mpu1_reading)
        # input2_source = MPUInputSource(0b00000010, received_new_mpu2_reading)
        # return input1_source, input2_source
    elif mpu1_source == "MOCK_MPU1" and mpu2_source == "MOCK_MPU2":
        print("# Mock source")
        input1_source = MockInputSource("pi/test1_mpu1", received_new_mpu1_reading)
        input2_source = MockInputSource("pi/test1_mpu2", received_new_mpu2_reading)
        return input1_source, input2_source
    elif 'LIVE' in mpu1_source and 'LIVE' in mpu2_source:
        input1_source = LiveInputSource("ios/accel-jake1?format=ALL", received_new_mpu1_reading)
        input2_source = LiveInputSource("ios/accel-jake2?format=ALL", received_new_mpu2_reading)
        return input1_source, input2_source
    else:
        print("# mpu1_source =" + mpu1_source, "  --- mpu2_source =" + mpu2_source)
        input1_source = MockInputSource(mpu1_source, received_new_mpu1_reading)
        input2_source = MockInputSource(mpu2_source, received_new_mpu2_reading)
        return input1_source, input2_source
