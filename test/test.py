from gpiozero import LED
from time import sleep

# ���Ŷ���
STEPPER_STEP_PIN = 25
STEPPER_DIR_PIN = 23
STEPPER_EN_PIN = 24

# ʹ�� LED �����������������
step_pin = LED(STEPPER_STEP_PIN)
dir_pin = LED(STEPPER_DIR_PIN)
en_pin = LED(STEPPER_EN_PIN)

# �����������͵�ƽ��Ч��
en_pin.off()
print("Driver enabled")

# ���÷���1Ϊһ������0Ϊ��һ������
dir_pin.on()
print("Direction: CW")

# �� blink() ���ɷ��������Ʋ������壩
# on_time = �ߵ�ƽ����ʱ��, off_time = �͵�ƽ����ʱ��
# n = �ظ�������None ��ʾ���ޣ�
print("Motor running...")
step_pin.blink(on_time=0.001, off_time=0.001, n=2000, background=False)

# ��ͣһ��
sleep(1)

# ������
dir_pin.off()
print("Direction: CCW")
step_pin.blink(on_time=0.01, off_time=0.01, n=200, background=False)

# ֹͣ����������
en_pin.on()
print("Driver disabled")
