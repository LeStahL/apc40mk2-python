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
            parsed['type'],
            parsed['channel'],
            parsed['note_number'],
            parsed['velocity'],
        )
    
    def serialize(self) -> bytes:
        result = MidiMessage.BinaryFormat.build(
            {
                'type': self.type,
                'channel': self.channel,
                'note_number': self.noteNumber,
                'velocity': self.velocity,
            }
        )
        return result
    
    def isNoteOn(self) -> bool:
        return self.type == 'note_on'
    
    def isNoteOff(self) -> bool:
        return self.type == 'note_off'
    
    def messageTypeString(self) -> str:
        if self.type == 'note_on':
            return 'NoteOn'
        elif self.type == 'note_off':
            return 'NoteOff'
        else:
            return 'Unknown'

    def __repr__(self) -> str:
        return '<MidiMessage: type={}, chan={}, note={}, vel={}>'.format(
            self.messageTypeString(),
            self.channel,
            self.noteNumber,
            self.velocity,
        )