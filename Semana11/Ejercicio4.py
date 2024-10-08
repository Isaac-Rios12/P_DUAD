class Head:
    def __init__(self):
        pass

class Torso:
    def __init__(self, head, right_arm, left_arm, right_leg, left_leg):
        self.head = head
        self.rigth_arm = right_arm
        self.left_arm = left_arm
        self.right_leg = right_leg
        self.left_leg = left_leg
class Arm:
    def __init__(self, hand):
        self.hand = hand

class Hand:
    def __init__(self) :
        pass

class Leg:
    def __init__(self, feet):
        self.feet = feet

class Feet:
    def __init__(self):
        pass


head = Head()
right_hand = Hand()
right_arm = Arm(right_hand)
left_hand = Hand()
left_arm = Arm(left_hand)
right_feet = Feet()
right_leg = Leg(right_feet)
left_feet = Feet()
left_leg = Leg(left_feet)
torso = Torso(head, right_arm, left_arm, right_leg, left_leg)

