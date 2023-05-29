from construct import Struct, Bitwise, BitsInteger, Enum
from rtmidi import MidiMessage

class NoteMessage:
    NoteOn = 0x9
    NoteOff = 0x8
    VelocityUnsupported = 0x7f

    BinaryFormat = "note_message" / Bitwise(Struct(
        "type" / Enum(
            BitsInteger(4),
            note_on = NoteOn,
            note_off = NoteOff,
        )
        "channel" / BitsInteger(4),
        "note_number" / Int8un,
        "velocity" / Int8un,
    ))

    def __init__(self,
        type: int = NoteOff,
        channel: int = 0,
        noteNumber: int = 0,
        velocity: int = VelocityUnsupported,
    ) -> None:
        self.type = type
        self.channel = channel
        self.noteNumber = noteNumber
        self.velocity = velocity
    
    @staticmethod
    def parse(data: bytes):
        parsed = NoteMessage.BinaryFormat.parse(data)
        return NoteMessage(
            parsed['note_message']['type'],
            parsed['note_message']['channel'],
            parsed['note_message']['note_number'],
            parsed['note_message']['velocity'],
        )
    
    def serialize(self) -> bytes:
        return NoteMessage.BinaryFormat.build({
            'note_message': {
                'type': self.type,
                'channel': self.channel,
                'note_number': self.noteNumber,
                'velocity': self.velocity,
            }
        })

    def rtMidiMessage(self) -> MidiMessage:
        if self.type == NoteMessage.NoteOn:
            return MidiMessage.noteOn()