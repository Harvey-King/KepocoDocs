"""STATIC NEGATIVE TEST ONLY: these errors must remain visible in the editor."""
import kepoco
import a_module_that_does_not_exist_for_kepoco

kepoco.display.drawEllipse(0, 0, 10, 10, 1)  # Wrong spelling; source has Ellispe.
kepoco.display.setFont('font3x5.bin', spacing=1)  # Wrong keyword; source has space.
kepoco.buttonA.pressed(123)  # Wrong number of arguments.
unknown_kepoco_variable.display.update()  # Undefined name must not be suppressed.
