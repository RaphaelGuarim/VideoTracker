import math


class ObjectTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.centers = {}  # Dictionary to store object IDs and their center points
        self.id_counter = 0  # Counter to assign unique IDs to new objects


    def update(self, object_rects):
        """
        Update the object tracker with new object rectangles.

        Args:
            object_rects (list): List of rectangles representing the objects.

        Returns:
            objects_bbs_ids (list): List of object rectangles with assigned IDs.
        """
        objects_bbs_ids = []  # List to store object rectangles with their assigned IDs

        # Process each new object rectangle
        for rect in object_rects:
            x, y, w, h = rect
            cx = (x + x + w) // 2  # X coordinate of the center point
            cy = (y + y + h) // 2  # Y coordinate of the center point

            # Check if the object has been detected before
            object_detected = False
            for id, center in self.centers.items():
                # Calculate the distance between the current center and the new center
                dist = math.hypot(cx - center[0], cy - center[1])

                if dist < 35:  # If the distance is below a threshold, consider it as the same object
                    self.centers[id] = (cx, cy)  # Update the center point of the existing object
                    objects_bbs_ids.append([x, y, w, h, id])  # Assign the existing ID to the object
                    object_detected = True
                    break

            if not object_detected:  # If it's a new object
                self.centers[self.id_counter] = (cx, cy)  # Assign a new ID to the object
                objects_bbs_ids.append([x, y, w, h, self.id_counter])  # Assign the new ID to the object
                self.id_counter += 1

        # Clean up the dictionary by removing IDs that are no longer used
        new_centers = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.centers[object_id]
            new_centers[object_id] = center

        self.centers = new_centers.copy()  # Update the dictionary with the cleaned centers
        return objects_bbs_ids  # Return the object rectangles with their assigned IDs
