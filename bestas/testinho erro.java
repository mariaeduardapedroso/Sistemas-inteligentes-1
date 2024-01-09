package mantova;

import robocode.*;
import robocode.util.*;
import java.awt.geom.*;
import robocode.ScannedRobotEvent;
import static robocode.util.Utils.normalRelativeAngleDegrees;

public class TheBeast extends AdvancedRobot {
    ...
    
    // O método para disparo preditivo
    private void predictiveShoot(ScannedRobotEvent e) {
        double bulletPower = Math.min(3.0, getEnergy() - .1);
        double bulletSpeed = 20 - bulletPower * 3;
        long time = (long)(last_scan_dist / bulletSpeed);

        double futureX = pos_enemy_x + Math.sin(angle_absolute) * e.getVelocity() * time;
        double futureY = pos_enemy_y + Math.cos(angle_absolute) * e.getVelocity() * time;
        double absDeg = (Math.toDegrees(Math.atan2(futureX - getX(), futureY - getY())) + 360) % 360;
        setTurnGunRight(normalRelativeAngleDegrees(absDeg - getGunHeading()));
        
        fire(bulletPower);
    }

    public void applySaindodeFininho(ScannedRobotEvent e) {
        int range = 10;
        ahead(20);
        if (getDistance() < range) {
            predictiveShoot(e);
        } else {
            // Scan para aglomerados e outros comportamentos 
        }
    }
    
    public void onScannedRobot(ScannedRobotEvent e) {
        switch (this.state) {
            case 1:
                // Sua lógica para o estado 1
                ...
                break;
            case 2:
                applySaindodeFininho(e);
                break;
            case 3:
                // Sua lógica para o estado 3
                ...
                break;
            case 4:
                // Sua lógica para o estado 4
                ...
                break;
        }
    }
    
    ...
}
