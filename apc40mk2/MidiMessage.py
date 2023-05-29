from construct import Struct, Bitwise, BitsInteger, Enum, Int8un, BitStruct, ByteSwapped

class MidiMessage:
    NoteOn = 0x9
    NoteOff = 0x8
    VelocityUnsupported = 0x7f

    BinaryFormat = "midi_message" / BitStruct(
        "type" / Enum(
            BitsInteger(4),
            note_on = NoteOn,
            note_off = NoteOff,
        ),
        "channel" / BitsInteger(4),
        "note_number" / BitsInteger(8),
        "velocity" / BitsInteger(8),
    )

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
        parsed = MidiMessage.BinaryFormat.parse(data)
        return MidiMessage(
            parsed['midi_message']['type'],
            parsed['midi_message']['channel'],
            parsed['midi_message']['note_number'],
            parsed['midi_message']['velocity'],
        )
    
    def serialize(self) -> bytes:
        print(self.type, self.channel, self.noteNumber, self.velocity)
        result = MidiMessage.BinaryFormat.build(
            {
                'type': self.type,
                'channel': self.channel,
                'note_number': self.noteNumber,
                'velocity': self.velocity,
            }
        )
        print(result)
        return result
