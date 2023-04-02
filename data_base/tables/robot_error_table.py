from data_base.db import BaseModel
from sqlalchemy import Integer, Column, Date, Text, Time
from sqlalchemy.dialects.sqlite import DATE, TIME


class RobotErrorTable(BaseModel):
    __tablename__ = 'robot_error'

    ID = Column(Integer, primary_key=True)
    robot = Column(Text)
    date = Column(DATE)
    time = Column(TIME)
    who_repair = Column(Text)
    auto_repair = Column(Text)
    CMD_error = Column(Text)
    SECTION_error = Column(Integer)
    faults = Column(Text)
    user_id = Column(Integer)

    def __str__(self):
        return f'{self.robot}'