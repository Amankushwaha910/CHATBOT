
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JRadioButton;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class Quiztest extends JFrame implements ActionListener {
   private JLabel lblUser;
   private JLabel lblQuestion;
   private JLabel lblTimer;
   private JRadioButton[] options = new JRadioButton[4];
   private ButtonGroup bg;
   private JButton btnNext;
   private JButton btnResult;
   private String username = "Player";
   private int[] order = new int[]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
   private int current = 0;
   private int score = 0;
   private Timer countdownTimer;
   private int timeLeft = 15;

   public Quiztest() {
      super("Quiz — Simple App");
      this.askUsername();
      this.shuffleQuestions();
      this.buildGui();
      this.setQuestion();
      this.startTimer();
   }

   private void askUsername() {
      String name = JOptionPane.showInputDialog(this, "Enter your name:", "Welcome", -1);
      if (name != null && !name.trim().isEmpty()) {
         this.username = name.trim();
      }

   }

   private void shuffleQuestions() {
      Random r = new Random();

      for(int i = 0; i < this.order.length; ++i) {
         int j = r.nextInt(this.order.length);
         int tmp = this.order[i];
         this.order[i] = this.order[j];
         this.order[j] = tmp;
      }

   }

   private void buildGui() {
      this.setDefaultCloseOperation(3);
      this.setSize(700, 380);
      this.setLocationRelativeTo((Component)null);
      JPanel top = new JPanel(new BorderLayout());
      top.setBorder(BorderFactory.createEmptyBorder(10, 12, 10, 12));
      this.lblUser = new JLabel("User: " + this.username);
      this.lblUser.setFont(this.lblUser.getFont().deriveFont(1, 14.0F));
      top.add(this.lblUser, "West");
      this.lblTimer = new JLabel("Time: 15s", 4);
      this.lblTimer.setFont(this.lblTimer.getFont().deriveFont(1, 14.0F));
      top.add(this.lblTimer, "East");
      this.add(top, "North");
      JPanel center = new JPanel();
      center.setLayout(new BoxLayout(center, 1));
      center.setBorder(BorderFactory.createEmptyBorder(8, 20, 8, 20));
      this.lblQuestion = new JLabel("Question will appear here");
      this.lblQuestion.setFont(this.lblQuestion.getFont().deriveFont(0, 16.0F));
      this.lblQuestion.setAlignmentX(0.0F);
      center.add(this.lblQuestion);
      center.add(Box.createRigidArea(new Dimension(0, 12)));
      this.bg = new ButtonGroup();

      for(int i = 0; i < 4; ++i) {
         this.options[i] = new JRadioButton("Option " + (i + 1));
         this.options[i].setAlignmentX(0.0F);
         this.options[i].setFont(this.options[i].getFont().deriveFont(14.0F));
         this.bg.add(this.options[i]);
         center.add(this.options[i]);
         center.add(Box.createRigidArea(new Dimension(0, 6)));
      }

      this.add(center, "Center");
      JPanel bottom = new JPanel(new FlowLayout(1, 20, 10));
      this.btnNext = new JButton("Next");
      this.btnResult = new JButton("Result");
      this.btnResult.setVisible(false);
      this.btnNext.addActionListener(this);
      this.btnResult.addActionListener(this);
      bottom.add(this.btnNext);
      bottom.add(this.btnResult);
      this.add(bottom, "South");
      this.getContentPane().setBackground(Color.WHITE);
      top.setBackground(Color.WHITE);
      center.setBackground(Color.WHITE);
      bottom.setBackground(Color.WHITE);
      this.setVisible(true);
   }

   private void startTimer() {
      if (this.countdownTimer != null && this.countdownTimer.isRunning()) {
         this.countdownTimer.stop();
      }

      this.timeLeft = 15;
      this.lblTimer.setText("Time: " + this.timeLeft + "s");
      this.countdownTimer = new Timer(1000, (e) -> {
         --this.timeLeft;
         this.lblTimer.setText("Time: " + this.timeLeft + "s");
         if (this.timeLeft <= 0) {
            this.countdownTimer.stop();
            JOptionPane.showMessageDialog(this, "Time's up! Moving to next question.", "Time Up", 1);
            this.autoAdvanceDueToTimeout();
         }

      });
      this.countdownTimer.setInitialDelay(0);
      this.countdownTimer.start();
   }

   private void autoAdvanceDueToTimeout() {
      ++this.current;
      if (this.current >= this.order.length) {
         this.showResultScreen();
      } else {
         this.setQuestion();
         this.startTimer();
      }

   }

   private void setQuestion() {
      this.bg.clearSelection();
      int q = this.order[this.current];
      switch (q) {
         case 0:
            this.lblQuestion.setText("<html><b>Q: Which one is not a primitive datatype?</b></html>");
            this.options[0].setText("int");
            this.options[1].setText("Float");
            this.options[2].setText("boolean");
            this.options[3].setText("char");
            break;
         case 1:
            this.lblQuestion.setText("<html><b>Q: Which class is available to all classes automatically?</b></html>");
            this.options[0].setText("Swing");
            this.options[1].setText("Applet");
            this.options[2].setText("Object");
            this.options[3].setText("ActionEvent");
            break;
         case 2:
            this.lblQuestion.setText("<html><b>Q: Which package is always available without import?</b></html>");
            this.options[0].setText("swing");
            this.options[1].setText("applet");
            this.options[2].setText("net");
            this.options[3].setText("lang");
            break;
         case 3:
            this.lblQuestion.setText("<html><b>Q: String class is defined in which package?</b></html>");
            this.options[0].setText("lang");
            this.options[1].setText("swing");
            this.options[2].setText("applet");
            this.options[3].setText("awt");
            break;
         case 4:
            this.lblQuestion.setText("<html><b>Q: Which of the following is not a keyword?</b></html>");
            this.options[0].setText("class");
            this.options[1].setText("int");
            this.options[2].setText("get");
            this.options[3].setText("if");
            break;
         case 5:
            this.lblQuestion.setText("<html><b>Q: Which keyword is used to define a class?</b></html>");
            this.options[0].setText("object");
            this.options[1].setText("define");
            this.options[2].setText("class");
            this.options[3].setText("struct");
            break;
         case 6:
            this.lblQuestion.setText("<html><b>Q: Which of the following is a looping statement in Java?</b></html>");
            this.options[0].setText("switch");
            this.options[1].setText("for");
            this.options[2].setText("break");
            this.options[3].setText("if");
            break;
         case 7:
            this.lblQuestion.setText("<html><b>Q: Which exception is thrown when dividing by zero?</b></html>");
            this.options[0].setText("NullPointerException");
            this.options[1].setText("ArithmeticException");
            this.options[2].setText("NumberFormatException");
            this.options[3].setText("IOException");
            break;
         case 8:
            this.lblQuestion.setText("<html><b>Q: Which of these is not a Java access modifier?</b></html>");
            this.options[0].setText("public");
            this.options[1].setText("protected");
            this.options[2].setText("private");
            this.options[3].setText("internal");
            break;
         case 9:
            this.lblQuestion.setText("<html><b>Q: Which keyword is used to inherit a class in Java?</b></html>");
            this.options[0].setText("super");
            this.options[1].setText("extends");
            this.options[2].setText("implements");
            this.options[3].setText("this");
      }

      if (this.current == this.order.length - 1) {
         this.btnNext.setEnabled(false);
         this.btnResult.setVisible(true);
      } else {
         this.btnNext.setEnabled(true);
         this.btnResult.setVisible(false);
      }

   }

   private boolean checkAns() {
      int q = this.order[this.current];
      switch (q) {
         case 0 -> {
            return this.options[1].isSelected();
         }
         case 1 -> {
            return this.options[2].isSelected();
         }
         case 2 -> {
            return this.options[3].isSelected();
         }
         case 3 -> {
            return this.options[0].isSelected();
         }
         case 4 -> {
            return this.options[2].isSelected();
         }
         case 5 -> {
            return this.options[2].isSelected();
         }
         case 6 -> {
            return this.options[1].isSelected();
         }
         case 7 -> {
            return this.options[1].isSelected();
         }
         case 8 -> {
            return this.options[3].isSelected();
         }
         case 9 -> {
            return this.options[1].isSelected();
         }
         default -> {
            return false;
         }
      }
   }

   public void actionPerformed(ActionEvent e) {
      Object src = e.getSource();
      if (src == this.btnNext) {
         if (this.countdownTimer != null && this.countdownTimer.isRunning()) {
            this.countdownTimer.stop();
         }

         if (this.checkAns()) {
            ++this.score;
         }

         ++this.current;
         if (this.current >= this.order.length) {
            this.showResultScreen();
         } else {
            this.setQuestion();
            this.startTimer();
         }
      } else if (src == this.btnResult) {
         if (this.countdownTimer != null && this.countdownTimer.isRunning()) {
            this.countdownTimer.stop();
         }

         if (this.checkAns()) {
            ++this.score;
         }

         this.showResultScreen();
      }

   }

   private void showResultScreen() {
      int total = this.order.length;
      int percentage = Math.round((float)this.score * 100.0F / (float)total);
      JFrame resultFrame = new JFrame("Quiz Result");
      resultFrame.setSize(420, 260);
      resultFrame.setLocationRelativeTo(this);
      resultFrame.setDefaultCloseOperation(2);
      resultFrame.setLayout(new BorderLayout(10, 10));
      JPanel p = new JPanel();
      p.setLayout(new BoxLayout(p, 1));
      p.setBorder(BorderFactory.createEmptyBorder(12, 12, 12, 12));
      JLabel congrats = new JLabel("Congratulations, " + this.username + "!");
      congrats.setFont(congrats.getFont().deriveFont(1, 18.0F));
      congrats.setAlignmentX(0.5F);
      p.add(congrats);
      p.add(Box.createRigidArea(new Dimension(0, 12)));
      JLabel scoreLabel = new JLabel("Score: " + this.score + " / " + total);
      scoreLabel.setFont(scoreLabel.getFont().deriveFont(16.0F));
      scoreLabel.setAlignmentX(0.5F);
      p.add(scoreLabel);
      p.add(Box.createRigidArea(new Dimension(0, 8)));
      JLabel perLabel = new JLabel("Percentage: " + percentage + "%");
      perLabel.setFont(perLabel.getFont().deriveFont(16.0F));
      perLabel.setAlignmentX(0.5F);
      p.add(perLabel);
      p.add(Box.createRigidArea(new Dimension(0, 14)));
      JProgressBar bar = new JProgressBar(0, 100);
      bar.setValue(percentage);
      bar.setStringPainted(true);
      bar.setPreferredSize(new Dimension(350, 24));
      bar.setAlignmentX(0.5F);
      p.add(bar);
      p.add(Box.createRigidArea(new Dimension(0, 14)));
      JPanel btnPanel = new JPanel(new FlowLayout(1, 12, 0));
      JButton btnRestart = new JButton("Restart");
      JButton btnClose = new JButton("Close");
      btnRestart.addActionListener((ae) -> {
         resultFrame.dispose();
         this.restartQuiz();
      });
      btnClose.addActionListener((ae) -> {
         resultFrame.dispose();
         this.dispose();
      });
      btnPanel.add(btnRestart);
      btnPanel.add(btnClose);
      p.add(btnPanel);
      resultFrame.add(p, "Center");
      resultFrame.setVisible(true);
   }

   private void restartQuiz() {
      this.score = 0;
      this.current = 0;
      this.shuffleQuestions();
      this.setQuestion();
      this.startTimer();
      this.setVisible(true);
   }

   public static void main(String[] args) {
      SwingUtilities.invokeLater(() -> new Quiztest());
   }
}
